from policyengine_us.model_api import *


EXTRA_PUF_VARIABLES = [
    "e02000",
    "e26270",
    "e19200",
    "e18500",
    "e19800",
    "e20400",
    "e20100",
    "e00700",
    "e03270",
    "e24515",
    "e03300",
    "e07300",
    "e62900",
    "e32800",
    "e87530",
    "e03240",
    "e01100",
    "e01200",
    "e24518",
    "e09900",
    "e27200",
    "e03290",
    "e58990",
    "e03230",
    # "e07400",
    "e11200",
    "e07260",
    "e07240",
    # "e07600",
    "e03220",
    "p08000",
    "e03400",
    "e09800",
    "e09700",
    "e03500",
    "e87521",
]

for variable in EXTRA_PUF_VARIABLES:
    try:
        globals()[variable] = type(
            variable,
            (Variable,),
            {
                "label": variable,
                "value_type": float,
                "entity": Person,
                "definition_period": YEAR,
            },
        )
    except:
        pass
