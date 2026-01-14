"""Rhode Island Governor McKee's Child Tax Credit Analysis."""

from ri_mckee_ctc.reform import ri_mckee_ctc_reform
from ri_mckee_ctc.household import calculate_net_income_changes
from ri_mckee_ctc.statewide import (
    DECILE_OUTCOMES,
    OVERALL_OUTCOMES,
    REVENUE_IMPACT_MILLIONS,
    AVG_HOUSEHOLD_BENEFIT,
    AVG_BENEFIT_BY_DECILE,
    POVERTY_IMPACT,
    DEEP_POVERTY_IMPACT,
    GINI_IMPACT,
    CHILDREN_AFFECTED,
    PCT_FAMILIES_BENEFITING,
)
from ri_mckee_ctc.charts import (
    create_net_income_change_chart,
    create_winners_by_decile_chart,
    create_avg_benefit_by_decile_chart,
)

__all__ = [
    "ri_mckee_ctc_reform",
    "calculate_net_income_changes",
    "DECILE_OUTCOMES",
    "OVERALL_OUTCOMES",
    "REVENUE_IMPACT_MILLIONS",
    "AVG_HOUSEHOLD_BENEFIT",
    "AVG_BENEFIT_BY_DECILE",
    "POVERTY_IMPACT",
    "DEEP_POVERTY_IMPACT",
    "GINI_IMPACT",
    "CHILDREN_AFFECTED",
    "PCT_FAMILIES_BENEFITING",
    "create_net_income_change_chart",
    "create_winners_by_decile_chart",
    "create_avg_benefit_by_decile_chart",
]
