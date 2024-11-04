from typing import Any

from pydantic import Field, field_validator

from lion_core.abc import Communicatable
from lion_core.communication.utils import validate_sender_recipient
from lion_core.generic.element import Element
from lion_core.types import ID


class BaseMail(Element, Communicatable):
    """
    Base class for mail-like communication in the LION system.

    Attributes:
        sender (str): The ID of the sender node.
        recipient (str): The ID of the recipient node.
    """

    sender: ID.SenderRecipient = Field(
        default="N/A",
        title="Sender",
        description="The ID of the sender node or a role.",
    )

    recipient: ID.SenderRecipient = Field(
        default="N/A",
        title="Recipient",
        description="The ID of the recipient node, or a role",
    )

    @field_validator("sender", "recipient", mode="before")
    @classmethod
    def _validate_sender_recipient(cls, value: Any) -> ID.SenderRecipient:
        return validate_sender_recipient(value)


# File: lion_core/communication/base.py
