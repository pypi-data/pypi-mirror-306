"""Fused MoE utilities for AWQ/GPTQ."""

# In this module, we do fused topk, this is split from the upstream
# function in _fused_marlin_moe, so that we don't have to resolve
# a bunch of merge conflicts when syncing with new upstream versions.

from typing import Any, Callable, Dict, Optional

import torch

from ._fused_marlin_moe import fused_marlin_moe as fused_marlin_moe_unwrapped
from .fused_moe import fused_topk, grouped_topk


def fused_marlin_moe(
    *,
    hidden_states: torch.Tensor,
    w1: torch.Tensor,
    w2: torch.Tensor,
    w1_scale: Optional[torch.Tensor] = None,
    w2_scale: Optional[torch.Tensor] = None,
    gating_output: torch.Tensor,
    g_idx1: torch.Tensor,
    g_idx2: torch.Tensor,
    sort_indices1: torch.Tensor,
    sort_indices2: torch.Tensor,
    w1_zeros: Optional[torch.Tensor] = None,
    w2_zeros: Optional[torch.Tensor] = None,
    is_k_full: bool,
    topk: int,
    renormalize: bool,
    num_bits: int = 8,
    override_config: Optional[Dict[str, Any]] = None,
    use_grouped_topk: bool = False,
    num_expert_group: Optional[int] = None,
    custom_routing_function: Optional[Callable] = None,
    topk_group: Optional[int] = None,
) -> torch.Tensor:
    """
    This function computes a Mixture of Experts (MoE) layer using two sets of
    weights, w1 and w2, and top-k gating mechanism.

    Parameters:
    - hidden_states (torch.Tensor): The input tensor to the MoE layer.
    - w1 (torch.Tensor): The first set of expert weights.
    - w2 (torch.Tensor): The second set of expert weights.
    - w1_scale (Optional[torch.Tensor]): Optional scale to be used for
        w1.
    - w2_scale (Optional[torch.Tensor]): Optional scale to be used for
        w2.
    - gating_output (torch.Tensor): The output of the gating operation
        (before softmax).
    - g_idx1 (torch.Tensor): The first set of act_order indices.
    - g_idx2 (torch.Tensor): The second set of act_order indices.
    - sort_indices1 (torch.Tensor): The first act_order input permutation.
    - sort_indices2 (torch.Tensor): The second act_order input permutation.
    - w1_zeros (Optional[torch.Tensor]): Optional zero points to be used for w1.
    - w2_zeros (Optional[torch.Tensor]): Optional zero points to be used for w2.
    - renormalize (bool): If True, renormalize the top-k weights to sum to 1.
    - override_config (Optional[Dict[str, Any]]): Optional override
        for the kernel configuration.
    - num_bits (bool): The number of bits in expert weights quantization.

    Returns:
    - torch.Tensor: The output tensor after applying the MoE layer.
    """
    # Check constraints.
    assert hidden_states.shape[0] == gating_output.shape[0], "Number of tokens mismatch"
    assert hidden_states.shape[1] == w1.shape[1] * 16, "Hidden size mismatch w1"
    assert hidden_states.shape[1] == w2.shape[2] // (
        num_bits // 2
    ), "Hidden size mismatch w2"
    assert gating_output.shape[1] == w1.shape[0], "Number of experts mismatch"
    assert hidden_states.is_contiguous(), "Hidden_states must be contiguous"
    assert w1.is_contiguous(), "Expert weights1 must be contiguous"
    assert w2.is_contiguous(), "Expert weights2 must be contiguous"
    assert hidden_states.dtype == torch.float16
    assert num_bits in [4, 8]

    # DeekSeekv2 uses grouped_top_k
    if use_grouped_topk:
        assert topk_group is not None
        assert num_expert_group is not None
        topk_weights, topk_ids = grouped_topk(
            hidden_states=hidden_states,
            gating_output=gating_output,
            topk=topk,
            renormalize=renormalize,
            num_expert_group=num_expert_group,
            topk_group=topk_group,
        )
    elif custom_routing_function is None:
        topk_weights, topk_ids = fused_topk(
            hidden_states=hidden_states,
            gating_output=gating_output,
            topk=topk,
            renormalize=renormalize,
        )
    else:
        topk_weights, topk_ids = custom_routing_function(
            hidden_states=hidden_states,
            gating_output=gating_output,
            topk=topk,
            renormalize=renormalize,
        )
    return fused_marlin_moe_unwrapped(
        hidden_states=hidden_states,
        w1=w1,
        w2=w2,
        w1_scale=w1_scale,
        w2_scale=w2_scale,
        gating_output=gating_output,
        topk_weights=topk_weights,
        topk_ids=topk_ids,
        g_idx1=g_idx1,
        g_idx2=g_idx2,
        sort_indices1=sort_indices1,
        sort_indices2=sort_indices2,
        w1_zeros=w1_zeros,
        w2_zeros=w2_zeros,
        override_config=override_config,
        num_bits=num_bits,
        is_k_full=is_k_full,
    )
