from dataclasses import dataclass, make_dataclass

from apischema import deserialize


@dataclass
class Point:
    x: int
    y: int


Point3 = make_dataclass(cls_name="Point3", bases=(Point,), fields=[("z", int)])

# Point4 = make_dataclass(cls_name="Point3", bases=(Point,), fields=[("pt", Point3, field(default_factory=Point3))])
Point4 = make_dataclass(cls_name="Point3", bases=(Point,), fields=[("pt", Point3)])


test = {
    "x": 1,
    "y": 2,
    "z": 3,
}

test2 = {
    "x": 10,
    "y": 11,
    # "pt": test,
}

print(deserialize(Point4, test2))
