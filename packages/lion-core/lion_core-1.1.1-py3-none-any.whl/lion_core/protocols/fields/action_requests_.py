from lion_core.models import FieldModel
from lion_core.protocols.operatives.action_model import ActionRequestModel

_description = (
    "List of actions to be performed if `action_required` "
    "is **True**. Leave empty if no action is required. "
    "**When providing actions, you must choose from the "
    "provided `tool_schemas`. Do not invent function or "
    "argument names.**"
)

ACTION_REQUESTS_FIELD = FieldModel(
    name="action_requests",
    annotation=list[ActionRequestModel],
    default_factory=list,
    title="Actions",
    description=_description,
)
