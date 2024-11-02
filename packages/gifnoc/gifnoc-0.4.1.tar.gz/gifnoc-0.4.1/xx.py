from dataclasses import dataclass
from datetime import date

import gifnoc
from gifnoc.config import city
from gifnoc.registry import map_environment_variables


@dataclass
class Person:
    name: str
    birthdate: date


@gifnoc.register("city")
@dataclass
class City:
    name: str
    people: list[Person]

    # wat
    big: bool = False


map_environment_variables(
    CITY_NAME="city.name",
    BIGNESS="city.big",
)


# with load_sources("./example/ppl.yaml", os.environ) as x:
#     print(config.city)

with gifnoc.gifnoc(option_map={"--big": "city.big"}):
    print(city.big)
    # print(os.environ["BIGNESS"])
    # print(config)
    # print(config.city)
