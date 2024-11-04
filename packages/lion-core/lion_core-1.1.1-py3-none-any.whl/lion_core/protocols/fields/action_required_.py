from lion_core.funcs import validate_boolean
from lion_core.models import FieldModel

_description = (
    "Specify whether the step requires actions to be "
    "performed. If **True**, the actions in `action_requests` "
    "must be performed. If **False**, the actions in "
    "`action_requests` are optional. If no tool_schemas"
    " are provided, this field is ignored."
)


def validate_action_required(cls, value) -> bool:
    try:
        return validate_boolean(value)
    except Exception:
        return False


ACTION_REQUIRED_FIELD = FieldModel(
    name="action_required",
    annotation=bool,
    default=False,
    title="Action Required",
    description=_description,
    validator=validate_action_required,
    validator_kwargs={"mode": "before"},
)
