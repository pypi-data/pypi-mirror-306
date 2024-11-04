from typing import Literal

from pydantic import BaseModel


class LionUndefinedType:
    def __init__(self) -> None:
        self.undefined = True

    def __bool__(self) -> Literal[False]:
        return False

    def __deepcopy__(self, memo):
        # Ensure LN_UNDEFINED is universal
        return self

    def __repr__(self) -> Literal["LN_UNDEFINED"]:
        return "LN_UNDEFINED"

    __slots__ = ["undefined"]


LN_UNDEFINED = LionUndefinedType()


def clean_dump(obj: BaseModel) -> dict:
    dict_ = obj.model_dump(exclude_unset=True)
    for i in list(dict_.keys()):
        if dict_[i] is LN_UNDEFINED:
            dict_.pop(i)
    return dict_


__all__ = [
    "LionUndefinedType",
    "LN_UNDEFINED",
    "clean_dump",
]
