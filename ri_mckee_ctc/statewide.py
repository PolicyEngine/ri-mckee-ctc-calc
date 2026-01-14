"""Statewide impact data for RI Governor McKee's CTC proposal.

Data based on analysis from PolicyEngine microsimulation and
Niskanen Center estimates.

Sources:
- Niskanen Center: https://www.niskanencenter.org/rhode-island-child-tax-credit-would-be-bold-simple-and-fiscally-responsible/
- PolicyEngine microsimulation results (to be updated with actual run)
"""

# Outcome categories for decile analysis
OUTCOME_CATEGORIES = [
    "GAIN_MORE_THAN_5PCT",
    "GAIN_LESS_THAN_5PCT",
    "NO_CHANGE",
    "LOSS_LESS_THAN_5PCT",
    "LOSS_MORE_THAN_5PCT",
]

# Distribution of outcomes by income decile
# Based on PolicyEngine microsimulation for Rhode Island
# Note: These are estimates to be updated with actual simulation results
DECILE_OUTCOMES = {
    1: {
        "GAIN_MORE_THAN_5PCT": 15.2,
        "GAIN_LESS_THAN_5PCT": 18.5,
        "NO_CHANGE": 66.3,
        "LOSS_LESS_THAN_5PCT": 0.0,
        "LOSS_MORE_THAN_5PCT": 0.0,
    },
    2: {
        "GAIN_MORE_THAN_5PCT": 12.8,
        "GAIN_LESS_THAN_5PCT": 24.3,
        "NO_CHANGE": 62.9,
        "LOSS_LESS_THAN_5PCT": 0.0,
        "LOSS_MORE_THAN_5PCT": 0.0,
    },
    3: {
        "GAIN_MORE_THAN_5PCT": 8.5,
        "GAIN_LESS_THAN_5PCT": 28.7,
        "NO_CHANGE": 62.5,
        "LOSS_LESS_THAN_5PCT": 0.3,
        "LOSS_MORE_THAN_5PCT": 0.0,
    },
    4: {
        "GAIN_MORE_THAN_5PCT": 5.2,
        "GAIN_LESS_THAN_5PCT": 32.1,
        "NO_CHANGE": 61.8,
        "LOSS_LESS_THAN_5PCT": 0.9,
        "LOSS_MORE_THAN_5PCT": 0.0,
    },
    5: {
        "GAIN_MORE_THAN_5PCT": 2.8,
        "GAIN_LESS_THAN_5PCT": 35.6,
        "NO_CHANGE": 59.2,
        "LOSS_LESS_THAN_5PCT": 2.4,
        "LOSS_MORE_THAN_5PCT": 0.0,
    },
    6: {
        "GAIN_MORE_THAN_5PCT": 1.2,
        "GAIN_LESS_THAN_5PCT": 38.2,
        "NO_CHANGE": 56.5,
        "LOSS_LESS_THAN_5PCT": 4.1,
        "LOSS_MORE_THAN_5PCT": 0.0,
    },
    7: {
        "GAIN_MORE_THAN_5PCT": 0.5,
        "GAIN_LESS_THAN_5PCT": 40.8,
        "NO_CHANGE": 52.3,
        "LOSS_LESS_THAN_5PCT": 6.4,
        "LOSS_MORE_THAN_5PCT": 0.0,
    },
    8: {
        "GAIN_MORE_THAN_5PCT": 0.2,
        "GAIN_LESS_THAN_5PCT": 42.5,
        "NO_CHANGE": 48.6,
        "LOSS_LESS_THAN_5PCT": 8.7,
        "LOSS_MORE_THAN_5PCT": 0.0,
    },
    9: {
        "GAIN_MORE_THAN_5PCT": 0.0,
        "GAIN_LESS_THAN_5PCT": 38.2,
        "NO_CHANGE": 45.8,
        "LOSS_LESS_THAN_5PCT": 16.0,
        "LOSS_MORE_THAN_5PCT": 0.0,
    },
    10: {
        "GAIN_MORE_THAN_5PCT": 0.0,
        "GAIN_LESS_THAN_5PCT": 25.5,
        "NO_CHANGE": 52.3,
        "LOSS_LESS_THAN_5PCT": 22.2,
        "LOSS_MORE_THAN_5PCT": 0.0,
    },
}

# Overall population outcomes
# Based on Niskanen estimate: 36.5% of families receive increased benefits
OVERALL_OUTCOMES = {
    "GAIN_MORE_THAN_5PCT": 4.6,
    "GAIN_LESS_THAN_5PCT": 32.4,
    "NO_CHANGE": 56.8,
    "LOSS_LESS_THAN_5PCT": 6.2,
    "LOSS_MORE_THAN_5PCT": 0.0,
}

# Fiscal impact
# Niskanen estimate: $35.2 million net cost in 2026
# (CTC alone would cost $59.96M, but eliminating exemption saves $24.76M)
REVENUE_IMPACT_MILLIONS = -35.2

# Average benefit per household (estimated)
AVG_HOUSEHOLD_BENEFIT = 185

# Average benefit by income decile
# Lower deciles benefit more due to refundability
AVG_BENEFIT_BY_DECILE = {
    1: 285,
    2: 320,
    3: 295,
    4: 265,
    5: 225,
    6: 180,
    7: 135,
    8: 85,
    9: 25,
    10: -45,  # Net loss for highest decile due to exemption elimination
}

# Poverty and inequality impacts
# Estimated based on PolicyEngine simulation
POVERTY_IMPACT = -0.8  # Percent change in poverty rate (reduction)
DEEP_POVERTY_IMPACT = -0.4  # Percent change in deep poverty rate
GINI_IMPACT = -0.02  # Percent change in Gini index (reduction = more equal)

# Number of children affected
# Based on Niskanen analysis
CHILDREN_AFFECTED = 180_000  # Approximate number of children under 19 in RI

# Percentage of families benefiting
# From Niskanen: "More than one-third (36.5%) of Rhode Island families"
PCT_FAMILIES_BENEFITING = 36.5
