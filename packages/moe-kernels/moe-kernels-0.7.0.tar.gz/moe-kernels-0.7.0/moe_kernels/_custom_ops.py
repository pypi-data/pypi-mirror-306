import contextlib
import functools
from typing import TYPE_CHECKING, List, Optional, Tuple, Union

import torch
import torch.library

# Insure that the ops are registered.
import moe_kernels._moe_kernels

from .scalar_type import ScalarType

if TYPE_CHECKING:

    def register_fake(fn):
        return lambda name: fn

else:
    try:
        from torch.library import register_fake
    except ImportError:
        from torch.library import impl_abstract as register_fake


# activation ops
def silu_and_mul(out: torch.Tensor, x: torch.Tensor) -> None:
    torch.ops._moe_kernels.silu_and_mul(out, x)


def gelu_and_mul(out: torch.Tensor, x: torch.Tensor) -> None:
    torch.ops._moe_kernels.gelu_and_mul(out, x)


def gelu_tanh_and_mul(out: torch.Tensor, x: torch.Tensor) -> None:
    torch.ops._moe_kernels.gelu_tanh_and_mul(out, x)


def fatrelu_and_mul(out: torch.Tensor, x: torch.Tensor, threshold: float = 0.0) -> None:
    torch.ops._moe_kernels.fatrelu_and_mul(out, x, threshold)


def gelu_fast(out: torch.Tensor, x: torch.Tensor) -> None:
    torch.ops._moe_kernels.gelu_fast(out, x)


def gelu_new(out: torch.Tensor, x: torch.Tensor) -> None:
    torch.ops._moe_kernels.gelu_new(out, x)


def gelu_quick(out: torch.Tensor, x: torch.Tensor) -> None:
    torch.ops._moe_kernels.gelu_quick(out, x)


# moe
def moe_sum(input: torch.Tensor, output: torch.Tensor):
    torch.ops._moe_kernels.moe_sum(input, output)


def moe_align_block_size(
    topk_ids: torch.Tensor,
    num_experts: int,
    block_size: int,
    sorted_token_ids: torch.Tensor,
    experts_ids: torch.Tensor,
    num_tokens_post_pad: torch.Tensor,
) -> None:
    torch.ops._moe_kernels.moe_align_block_size(
        topk_ids,
        num_experts,
        block_size,
        sorted_token_ids,
        experts_ids,
        num_tokens_post_pad,
    )


def topk_softmax(
    topk_weights: torch.Tensor,
    topk_ids: torch.Tensor,
    token_expert_indicies: torch.Tensor,
    gating_output: float,
) -> None:
    torch.ops._moe_kernels.topk_softmax(
        topk_weights, topk_ids, token_expert_indicies, gating_output
    )


if hasattr(torch.ops._moe_kernels, "marlin_gemm_moe"):

    @register_fake("_moe_kernels::marlin_gemm_moe")
    def marlin_gemm_moe_fake(
        a: torch.Tensor,
        b_q_weights: torch.Tensor,
        sorted_ids: torch.Tensor,
        topk_weights: torch.Tensor,
        topk_ids: torch.Tensor,
        b_scales: torch.Tensor,
        b_zero_points: torch.Tensor,
        g_idx: torch.Tensor,
        perm: torch.Tensor,
        workspace: torch.Tensor,
        b_q_type: ScalarType,
        size_m: torch.SymInt,
        size_n: torch.SymInt,
        size_k: torch.SymInt,
        is_k_full: bool,
        num_experts: int,
        topk: int,
        moe_block_size: int,
        replicate_input: bool,
        apply_weights: bool,
    ) -> torch.Tensor:
        return torch.empty((size_m, topk, size_n), dtype=a.dtype, device=a.device)
