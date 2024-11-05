from lion_core.models import FieldModel
from lion_core.protocols.operatives.action_model import ActionResponseModel

ACTION_RESPONSES_FIELD = FieldModel(
    name="action_responses",
    annotation=list[ActionResponseModel],
    default_factory=list,
    title="Actions",
    description="**do not fill**",
)
