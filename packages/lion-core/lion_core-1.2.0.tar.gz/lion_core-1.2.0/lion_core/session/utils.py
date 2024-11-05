from typing import Literal

from pydantic import BaseModel, JsonValue

from lion_core.communication.action_request import ActionRequest
from lion_core.communication.action_response import ActionResponse
from lion_core.communication.assistant_response import AssistantResponse
from lion_core.communication.instruction import Instruction
from lion_core.communication.system import System
from lion_core.protocols.operatives.action_model import (
    ActionRequestModel,
    ActionResponseModel,
)
from lion_core.types import ID

from .msg_handlers import (
    create_action_request,
    create_action_response,
    create_assistant_response,
    create_instruction,
    create_system,
)


def create_message(
    sender: ID.SenderRecipient = None,
    recipient: ID.SenderRecipient = None,
    instruction: Instruction | JsonValue = None,
    context: JsonValue = None,
    guidance: JsonValue = None,
    plain_content: str = None,
    request_fields: list[str] | dict = None,
    request_model: type[BaseModel] | BaseModel = None,
    system: System | JsonValue = None,
    system_sender: ID.SenderRecipient = None,
    system_datetime: bool | str = None,
    images: list = None,
    image_detail: Literal["low", "high", "auto"] | None = None,
    assistant_response: AssistantResponse | JsonValue = None,
    action_request: ActionRequest = None,
    action_response: ActionResponse = None,
    action_request_model: ActionRequestModel = None,
    action_response_model: ActionResponseModel = None,
):
    """Create a message based on the provided parameters.

    Args:
        sender: The sender of the message.
        recipient: The recipient of the message.
        instruction: Instruction content or object.
        context: Additional context for the message.
        guidance: Guidance information.
        plain_content: Plain text content.
        request_fields: Fields for the request.
        request_model: Model for the request.
        system: System message content or object.
        system_sender: The sender of the system message.
        system_datetime: System datetime information.
        images: List of images.
        image_detail: Image detail level.
        assistant_response: Assistant response content or object.
        action_request: Action request message.
        action_response: Action response message.
        action_request_model: Action request model.
        action_response_model: Action response model.

    Returns:
        A message object of the appropriate type.

    Raises:
        ValueError: If multiple message roles are provided or if an
            action response is provided without an action request.
    """
    """kwargs for additional instruction context"""
    if (
        len(
            [
                i
                for i in [instruction, system, assistant_response]
                if i is not None
            ],
        )
        > 1
    ):
        raise ValueError("Error: Message can only have one role")

    if action_response_model or action_response:
        if not action_request:
            raise ValueError(
                "Error: Action response must have an action request."
            )
        return create_action_response(
            action_request=action_request,
            action_response_model=action_response_model,
            action_response=action_response,
        )
    if action_request_model or action_request:
        return create_action_request(
            action_request_model=action_request_model,
            sender=sender,
            recipient=recipient,
            action_request=action_request,
        )
    if system:
        return create_system(
            system=system,
            sender=system_sender,
            recipient=recipient,
            system_datetime=system_datetime,
        )
    if assistant_response:
        return create_assistant_response(
            sender=sender,
            recipient=recipient,
            assistant_response=assistant_response,
        )
    return create_instruction(
        sender=sender,
        recipient=recipient,
        instruction=instruction,
        context=context,
        guidance=guidance,
        request_fields=request_fields,
        images=images,
        image_detail=image_detail,
        request_model=request_model,
        plain_content=plain_content,
    )
