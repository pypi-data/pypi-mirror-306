import dataclasses
from typing import Protocol, runtime_checkable

from ovld import ovld


@runtime_checkable
@dataclasses.dataclass
class Dataclass(Protocol):
    @classmethod
    def __subclasshook__(cls, subclass):
        return hasattr(subclass, "__dataclass_fields__") and hasattr(
            subclass, "__dataclass_params__"
        )


@ovld
def f(x: type[Dataclass], y: int):
    return "Dataclass"


@ovld
def f(x: type[int], y: int):
    return "int"


@ovld
def f(x: type[object], y: int):
    return "Not dataclass"


@dataclasses.dataclass
class Bob:
    a: int
    b: int


class Bab:
    a: int
    b: int


print(f(Bob, 1))
print(f(Bab, 1))
print(f(int, 1))
