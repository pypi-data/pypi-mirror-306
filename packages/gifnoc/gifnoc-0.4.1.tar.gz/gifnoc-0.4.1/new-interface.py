from dataclasses import dataclass


@dataclass
class A:
    x: int


@dataclass
class B:
    y: int
    z: int


class ABI(Interface):
    x = "a.x"
    y = "b.y"
    z = "b.z"
