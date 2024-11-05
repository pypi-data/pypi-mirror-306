from lion_core.models import FieldModel
from lion_core.protocols.operatives.reason import ReasonModel

_description = "**Provide a concise reason for the decision made.**"

REASON_FIELD = FieldModel(
    name="reason",
    annotation=ReasonModel | None,
    default=None,
    title="Reason",
    description=_description,
)
