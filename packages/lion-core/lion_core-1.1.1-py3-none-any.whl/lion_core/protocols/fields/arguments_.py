from lion_core.models import FieldModel

_arguments_description = (
    "Provide the arguments to pass to the function as a "
    "dictionary. **Use "
    "argument names and types as specified in the "
    "`tool_schemas`; do not "
    "invent argument names.**"
)


ARGUMENTS_FIELD = FieldModel(
    name="arguments",
    annotation=dict | None,
    default_factory=dict,
    title="Action Arguments",
    description=_arguments_description,
    examples=[{"num1": 1, "num2": 2}, {"x": "hello", "y": "world"}],
)
