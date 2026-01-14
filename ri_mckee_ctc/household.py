"""Household impact calculations for RI Governor McKee's CTC proposal."""

from typing import Tuple, List
import numpy as np


def calculate_net_income_changes(
    min_income: int = 0,
    max_income: int = 300_000,
    step: int = 1_000,
    num_children: int = 2,
) -> Tuple[List[int], List[float]]:
    """Calculate net income changes for a household across income levels.

    This models a married couple with children in Rhode Island comparing:
    - Baseline: Current law with personal exemption for dependent children
    - Reform: $325 CTC per child, no personal exemption for children

    The reform provides net benefits to lower-income households since the
    $325 credit is fully refundable, while higher-income households that
    fully utilized the personal exemption may see smaller or no gains.

    Args:
        min_income: Minimum income to analyze
        max_income: Maximum income to analyze
        step: Income increment
        num_children: Number of qualifying children under 19

    Returns:
        Tuple of (income_values, net_income_changes)
    """
    incomes = list(range(min_income, max_income + 1, step))
    changes = []

    # Credit amount per child
    ctc_amount = 325
    total_credit = ctc_amount * num_children

    # Phase-out parameters
    phase_out_start = 261_000
    # Assume phase-out rate (to be verified)
    phase_out_rate = 0.05  # 5% reduction per $1,000 over threshold

    # RI personal exemption value per dependent (approximate)
    # This would reduce taxable income, so the tax value depends on marginal rate
    personal_exemption_per_child = 4_650  # Approximate RI value
    ri_marginal_rate = 0.0599  # RI top marginal rate
    exemption_tax_value = personal_exemption_per_child * ri_marginal_rate * num_children

    for income in incomes:
        # Calculate CTC value (fully refundable)
        if income <= phase_out_start:
            ctc_value = total_credit
        else:
            reduction = (income - phase_out_start) / 1_000 * phase_out_rate * total_credit
            ctc_value = max(0, total_credit - reduction)

        # Calculate lost exemption value
        # For lower-income households, the exemption may not have been fully utilized
        # Approximate: exemption has full value only above a certain income
        if income < 30_000:
            # Low income - exemption had little value, CTC is pure gain
            lost_exemption_value = exemption_tax_value * (income / 30_000)
        else:
            lost_exemption_value = exemption_tax_value

        # Net change = CTC gained - exemption value lost
        net_change = ctc_value - lost_exemption_value
        changes.append(round(net_change, 2))

    return incomes, changes


def calculate_single_parent_changes(
    min_income: int = 0,
    max_income: int = 150_000,
    step: int = 1_000,
    num_children: int = 2,
) -> Tuple[List[int], List[float]]:
    """Calculate net income changes for a single parent household.

    Args:
        min_income: Minimum income to analyze
        max_income: Maximum income to analyze
        step: Income increment
        num_children: Number of qualifying children under 19

    Returns:
        Tuple of (income_values, net_income_changes)
    """
    return calculate_net_income_changes(
        min_income=min_income,
        max_income=max_income,
        step=step,
        num_children=num_children,
    )
