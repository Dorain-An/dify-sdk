from enum import IntEnum, StrEnum
from typing import Any, Self


class MetaConst(type):
    def __setattr__(cls, key: Any, value: Any) -> None:  # pragma: no cover
        raise TypeError(f"Constant {key} can't be modified ")


class Constant(metaclass=MetaConst):
    pass


class DocIntEnum(IntEnum):
    def __new__(cls, value: int, doc: str) -> "DocIntEnum":
        self = int.__new__(cls, value)
        self._value_ = value
        self.__doc__ = doc
        return self

    def __str__(self) -> str:
        return self.__doc__  # type:ignore


class DocStrEnum(StrEnum):
    def __new__(cls, value: str, doc: str) -> "DocStrEnum":
        self = str.__new__(cls, value)
        self._value_ = value
        self.__doc__ = doc
        return self

    def __str__(self) -> str:
        return self.__doc__  # type:ignore

    @classmethod
    def from_str(cls, value: str) -> Self:
        for item in cls:
            if item.value == value:
                return item
        raise ValueError(f"{value} is not a valid value for {cls.__name__}")
