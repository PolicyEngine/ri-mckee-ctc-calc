"""Rhode Island Governor McKee's Child Tax Credit reform definition.

This reform implements:
- $325 fully refundable child tax credit per child under 19
- Phase-out beginning at $261,000 for all filing statuses
- Eliminates the personal exemption for dependent children under 19

Note: The reform parameters should be updated once the exact parameter paths
are confirmed in policyengine-us.
"""

from policyengine_core.reforms import Reform

# Define the reform: RI CTC of $325 per child, phasing out at $261,000
# Also eliminates personal exemption for children under 19
#
# Parameters to modify (these paths need to be verified against policyengine-us):
# - gov.states.ri.tax.income.credits.ctc.amount: $325
# - gov.states.ri.tax.income.credits.ctc.phase_out.start: $261,000
# - gov.states.ri.tax.income.credits.ctc.max_age: 18 (under 19)
# - gov.states.ri.tax.income.exemptions.personal.dependent_child_under_19: $0

# TODO: Update with actual policyengine-us parameter paths once available
ri_mckee_ctc_reform = Reform.from_dict(
    {
        # RI CTC credit amount per child
        "gov.states.ri.tax.income.credits.ctc.amount": {
            "2026-01-01.2100-12-31": 325
        },
        # Phase-out threshold
        "gov.states.ri.tax.income.credits.ctc.phase_out.threshold": {
            "2026-01-01.2100-12-31": 261_000
        },
        # Maximum age (under 19 means max age 18)
        "gov.states.ri.tax.income.credits.ctc.age.max": {
            "2026-01-01.2100-12-31": 18
        },
        # Eliminate personal exemption for dependent children
        "gov.states.ri.tax.income.exemptions.dependent_child_amount": {
            "2026-01-01.2100-12-31": 0
        },
    },
    country_id="us",
)
