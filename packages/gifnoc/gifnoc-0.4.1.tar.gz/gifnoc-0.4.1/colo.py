from dataclasses import dataclass, field
from datetime import date

from apischema import ValidationError, deserializer

import gifnoc


@dataclass
class Color:
    red: int
    green: int
    blue: int


@dataclass
class Color2:
    pass


@deserializer
def color_from_string(s: str) -> Color:
    if not s.startswith("#") or not len(s) == 7:
        raise ValidationError("Color description should have format #123456")
    return Color(
        red=int(s[1:3], 16),
        green=int(s[3:5], 16),
        blue=int(s[5:7], 16),
    )


# @deserializer
# def color_from_dict(d: dict) -> Color:
#     return Color(**d)


@dataclass
class Colors:
    fg: Color = field(default_factory=lambda: Color(0, 0, 0))
    bg: Color = field(default_factory=lambda: Color(255, 255, 255))
    more: list[Color] = field(default_factory=list)
    start: date = date(year=2024, month=1, day=1)


colors = gifnoc.define(
    field="colors",
    model=Colors,
)


# print(deserialize(Color, "#f00"))


with gifnoc.cli(options="colors"):
    print(colors.more)
    print(colors.start.year)
