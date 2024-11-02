import threading
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import gifnoc

# from gifnoc.type_wrappers import TaggedSubclass


@dataclass
class Member:
    # Member name
    name: str
    # User name
    username: str
    # Home directory
    home: Path
    # Date the member started working
    start: date
    # Date the member stopped working
    end: date | None


@dataclass
class Machine:
    name: str
    os: str
    ngpus: int


@dataclass
class Organization:
    # Name of the organization
    name: str
    # Whether the organization is a nonprofit
    nonprofit: bool
    # Members of the organization
    members: list[Member]
    # Machines the organization owns
    machines: list[Machine]


org = gifnoc.define(
    field="org",
    model=Organization,
    environ={
        "ORG_NAME": "name",
        "NONPROFIT": "nonprofit",
    },
)


@dataclass
class Point:
    # ex
    x: int
    # why
    y: int


@dataclass
class Point3D(Point):
    # zeeee
    z: int


@dataclass
class Point4D(Point3D):
    # dubs
    w: int


@dataclass
class CLI:
    commind: str = "org"

    @property
    def command(self):
        return self.commind


clay = gifnoc.define(
    field="cli",
    model=CLI,
)


pointy = gifnoc.define(
    field="point",
    model=Point,
)


def loki(msg):
    try:
        print(msg, "has", org.name)
    except Exception:
        print(msg, "no.")
    # print(msg, current_configuration())


if __name__ == "__main__":
    loki("init")
    with gifnoc.cli(
        options="org",
    ):
        loki("nothread1")
        thr = threading.Thread(target=loki, args=["thread"])
        thr.start()
        thr.join()
        loki("nothread2")
        print("done.")
