import contextlib
from typing import List, Union

import torch
import torch.distributed as dist
import torch.distributed._functional_collectives as ft_c
import torch.distributed.distributed_c10d as c10d
import torch.nn.functional as F
from torch.distributed import DeviceMesh
from torch.distributed.tensor.experimental._attention import _templated_ring_attention
from torch.overrides import TorchFunctionMode

para_attn_ops = torch.ops.para_attn

__all__ = [
    "UnifiedAttnMode",
    "RingAttnMode",
    "UlyssesAttnMode",
    "ring_attn_func",
    "ulysses_attn_func",
]


def _maybe_wait(tensor: torch.Tensor) -> torch.Tensor:
    """
    When tracing the code, the result tensor is not an AsyncCollectiveTensor,
    so we cannot call ``wait()``.
    """
    if isinstance(tensor, ft_c.AsyncCollectiveTensor):
        return tensor.wait()
    return tensor


def _sdpa_all_to_all_single(x, mesh):
    if x.requires_grad:
        x = ft_c.all_to_all_single_autograd(x, output_split_sizes=None, input_split_sizes=None, group=mesh)
    else:
        x = ft_c.all_to_all_single(x, output_split_sizes=None, input_split_sizes=None, group=mesh)
    x = _maybe_wait(x)
    return x


def _sdpa_input_all_to_all(x, mesh):
    if isinstance(mesh, dist.ProcessGroup):
        pg: Union[dist.ProcessGroup, List[dist.ProcessGroup]] = mesh
    else:
        pg = mesh.get_group()
    assert isinstance(pg, dist.ProcessGroup), "process group must be single dimension"
    world_size = dist.get_world_size(pg)
    if world_size <= 1:
        return x

    assert x.ndim == 4, "x must have 4 dimensions, got {}".format(x.ndim)
    b, h, s, d = x.shape
    assert h % world_size == 0, "h must be divisible by world_size, got {} and {}".format(h, world_size)

    x = x.permute(1, 0, 2, 3).contiguous()
    x_shape = x.shape
    x = x.flatten()
    x = _sdpa_all_to_all_single(x, mesh)
    x = x.reshape(x_shape)
    x = x.reshape(world_size, h // world_size, b, -1, d).permute(2, 1, 0, 3, 4).reshape(b, h // world_size, -1, d)
    return x


def _sdpa_output_all_to_all(x, mesh):
    if isinstance(mesh, dist.ProcessGroup):
        pg: Union[dist.ProcessGroup, List[dist.ProcessGroup]] = mesh
    else:
        pg = mesh.get_group()
    assert isinstance(pg, dist.ProcessGroup), "process group must be single dimension"
    world_size = dist.get_world_size(pg)
    if world_size <= 1:
        return x

    assert x.ndim == 4, "x must have 4 dimensions, got {}".format(x.ndim)
    b, h, s, d = x.shape
    assert s % world_size == 0, "s must be divisible by world_size, got {} and {}".format(s, world_size)

    x = x.permute(2, 0, 1, 3).contiguous()
    x_shape = x.shape
    x = x.flatten()
    x = _sdpa_all_to_all_single(x, mesh)
    x = x.reshape(x_shape)
    x = x.reshape(world_size, s // world_size, b, -1, d).permute(2, 0, 3, 1, 4).reshape(b, -1, s // world_size, d)
    return x


def ulysses_attn_func(
    query,
    key,
    value,
    attn_mask=None,
    dropout_p=0.0,
    is_causal=False,
    *,
    scale=None,
    mesh=None,
):
    assert attn_mask is None, "attn_mask is not supported in ulysses_attn_func"

    assert query.ndim == 4, "query must have 4 dimensions, got {}".format(query.ndim)
    assert key.ndim == 4, "key must have 4 dimensions, got {}".format(key.ndim)
    assert value.ndim == 4, "value must have 4 dimensions, got {}".format(value.ndim)

    if mesh is None:
        mesh = c10d._get_default_group()

    query = _sdpa_input_all_to_all(query, mesh)
    key = _sdpa_input_all_to_all(key, mesh)
    value = _sdpa_input_all_to_all(value, mesh)

    out = F.scaled_dot_product_attention(
        query, key, value, attn_mask=attn_mask, dropout_p=dropout_p, is_causal=is_causal, scale=scale
    )

    out = _sdpa_output_all_to_all(out, mesh)
    return out


class RingAttnFunc(torch.autograd.Function):
    @staticmethod
    def forward(
        ctx,
        query,
        key,
        value,
        attn_mask,
        dropout_p,
        is_causal,
        scale,
        mesh,
    ):
        out, lse = _templated_ring_attention(
            mesh,
            para_attn_ops.attention_forward_with_lse,
            query,
            key,
            value,
            attn_mask=attn_mask,
            dropout_p=dropout_p,
            is_causal=is_causal,
            scale=scale,
        )
        return out

    @staticmethod
    def backward(ctx, dout, *args):
        raise NotImplementedError("Backward pass for RingAttnFunc is not implemented")


def ring_attn_func(
    query,
    key,
    value,
    attn_mask=None,
    dropout_p=0.0,
    is_causal=False,
    *,
    scale=None,
    mesh=None,
):
    assert attn_mask is None, "attn_mask is not supported in ring_attn_func"

    if mesh is None:
        mesh = c10d._get_default_group()
    if isinstance(mesh, dist.ProcessGroup):
        pg: Union[dist.ProcessGroup, List[dist.ProcessGroup]] = mesh
    else:
        pg = mesh.get_group()
    assert isinstance(pg, dist.ProcessGroup), "process group must be single dimension"
    world_size = dist.get_world_size(pg)
    if world_size <= 1:
        return F.scaled_dot_product_attention(
            query,
            key,
            value,
            attn_mask=attn_mask,
            dropout_p=dropout_p,
            is_causal=is_causal,
            scale=scale,
        )

    return RingAttnFunc.apply(
        query,
        key,
        value,
        attn_mask,
        dropout_p,
        is_causal,
        scale,
        mesh,
    )


def _get_arg(args, kwargs, *field):
    if len(field) == 1:
        if isinstance(field, int):
            if field < len(args):
                return args[field]
            else:
                return None
        else:
            return kwargs.get(field[0])
    else:
        index, name = field
        if index < len(args):
            return args[index]
        else:
            return kwargs.get(name)


def _get_args(args, kwargs, *names):
    results = []
    for i, name in enumerate(names):
        results.append(_get_arg(args, kwargs, i, name))
    return results


class RingAttnMode(TorchFunctionMode):
    def __init__(self, mesh=None):
        super().__init__()
        self._mesh = mesh

    def __torch_function__(self, func, types, args=(), kwargs=None):
        kwargs = {} if kwargs is None else kwargs

        if func is torch.nn.functional.scaled_dot_product_attention:
            return ring_attn_func(*args, **kwargs, mesh=self._mesh)
        return func(*args, **kwargs)


class UlyssesAttnMode(TorchFunctionMode):
    def __init__(self, mesh=None):
        super().__init__()
        self._mesh = mesh
        self._inside_func = False

    def __torch_function__(self, func, types, args=(), kwargs=None):
        kwargs = {} if kwargs is None else kwargs

        if func is torch.nn.functional.scaled_dot_product_attention:
            return ulysses_attn_func(*args, **kwargs, mesh=self._mesh)
        return func(*args, **kwargs)


class UnifiedAttnMode(TorchFunctionMode):
    def __init__(self, mesh):
        super().__init__()
        assert isinstance(mesh, DeviceMesh), "mesh must be a DeviceMesh"
        assert mesh.mesh.ndim == 2, "mesh must be 2D, got {}".format(mesh.mesh.ndim)
        self._parallel_method = "ulysses"
        self._ulysses_mesh = mesh["ulysses"]
        self._ring_mesh = mesh["ring"]

    def __torch_function__(self, func, types, args=(), kwargs=None):
        kwargs = {} if kwargs is None else kwargs

        if func is torch.nn.functional.scaled_dot_product_attention:
            parallel_method = self._parallel_method
            if parallel_method == "ulysses":
                with self._set_parallel_method("ring"), self:
                    return ulysses_attn_func(*args, **kwargs, mesh=self._ulysses_mesh)
            elif parallel_method == "ring":
                with self._set_parallel_method("none"), self:
                    return ring_attn_func(*args, **kwargs, mesh=self._ring_mesh)
            elif parallel_method == "none":
                return func(*args, **kwargs)
            else:
                raise ValueError(f"Unknown parallel method: {parallel_method}")

        return func(*args, **kwargs)

    @contextlib.contextmanager
    def _set_parallel_method(self, method):
        old_parallel_method = self._parallel_method
        self._parallel_method = method
        try:
            yield
        finally:
            self._parallel_method = old_parallel_method
