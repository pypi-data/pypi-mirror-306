function_field_description = (
    "Specify the name of the function to execute. **Choose "
    "from the provided `tool_schemas`; do not invent function names.**"
    "Only provide function names if tool_schemas are provided. Otherwise, "
    "must leave blank or set to None."
)

arguments_field_description = (
    "Provide the arguments to pass to the function as a "
    "dictionary. **Use argument names and types as specified in the "
    "`tool_schemas`; do not invent argument names.**"
)

action_required_field_description = (
    "Specify whether the step requires actions to be "
    "performed. If **True**, the actions in `action_requests` "
    "must be performed. If **False**, the actions in "
    "`action_requests` are optional. If no tool_schemas"
    " are provided, this field is ignored."
)

action_requests_field_description = (
    "List of actions to be performed if `action_required` "
    "is **True**. Leave empty if no action is required. "
    "**When providing actions, you must choose from the "
    "provided `tool_schemas`. Do not invent function or "
    "argument names.**"
)

confidence_description = (
    "Provide an objective numeric confidence score between 0 and 1 (with 3 "
    "decimal places) indicating how likely you successfully achieved the task"
    " according to user expectation. Interpret the score as:\n"
    "- **1**: Very confident in a good job.\n"
    "- **0**: Not confident at all.\n"
    "- **[0.8, 1]**: You can continue the path of reasoning if needed.\n"
    "- **[0.5, 0.8)**: Recheck your reasoning and consider reverting to a "
    "previous, more confident reasoning path.\n"
    "- **[0, 0.5)**: Stop because the reasoning is starting to be off track."
)
