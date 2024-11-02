from policyengine_us.model_api import *


class long_term_capital_gains_on_small_business_stock(Variable):
    value_type = float
    entity = Person
    label = "Long-term capital gains on small business stock sales, etc"
    unit = USD
    documentation = "Portion of capital_gains_28_percent_rate_gain not associated with collectibles."
    definition_period = YEAR
    reference = dict(
        title="26 U.S. Code § 1(h)(4)",
        href="https://www.law.cornell.edu/uscode/text/26/1#h_4",
    )
