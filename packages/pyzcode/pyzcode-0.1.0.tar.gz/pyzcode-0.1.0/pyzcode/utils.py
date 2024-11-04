from dataclasses import dataclass


def convert_to_int(value):
    if isinstance(value, int):
        return value
    else:
        value = value.strip()
    try:
        return int(value)
    except Exception as e:
        raise ValueError(f"Invalid value: {value}") from e


def convert_to_bool(value):
    if isinstance(value, bool):
        return value
    else:
        value = value.strip()
    if value.lower() == 1:
        return True
    elif value.lower() == 2:
        return False
    else:
        raise ValueError(f"Invalid value: {value}")


@dataclass
class ZipCode:
    zip: int
    type: str
    decommissioned: bool
    primary_city: str
    acceptable_cities: str
    unacceptable_cities: str
    county: str
    timezone: str
    area_codes: str
    world_region: str
    country: str
    irs_estimated_population: int

    def __post_init__(self):
        self.zip = convert_to_int(self.zip)
        self.decommissioned = convert_to_bool(self.decommissioned)
        self.irs_estimated_population = convert_to_int(
            self.irs_estimated_population
        )
