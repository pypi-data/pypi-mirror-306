from .data_loader import DataLoader
from .utils import convert_to_int


class ZipCode:
    def __init__(self, zip_code):
        query = ZipCodeQuery()
        data = query.get_zipcode(zip_code)
        if data:
            self.zip = data["zip"]
            self.type = data["type"]
            self.decommissioned = data["decommissioned"]
            self.primary_city = data["primary_city"]
            self.acceptable_cities = data["acceptable_cities"]
            self.unacceptable_cities = data["unacceptable_cities"]
            self.county = data["county"]
            self.timezone = data["timezone"]
            self.area_codes = data["area_codes"]
            self.world_region = data["world_region"]
            self.country = data["country"]
            self.irs_estimated_population = data["irs_estimated_population"]
        else:
            raise ValueError(f"No data found for zip code: {zip_code}")

    def __repr__(self):
        """Return the dictionary form of the object."""
        return str(self.__dict__)


class ZipCodeQuery:
    def __init__(self):
        self.data_loader = DataLoader()
        self.data = self.data_loader.data

    def _filter_data(self, **kwargs):
        """Helper function to filter data based on key-value pairs."""
        res = self.data
        for key, value in kwargs.items():
            if value is not None:
                if key in ["primary_city", "state", "type"]:
                    value = value.lower()
                    res = [x for x in res if x.get(key, "").lower() == value]
                else:
                    res = [x for x in res if x.get(key) == value]
        return res

    def get_zipcode(self, zip_code):
        """Retrieve a single zip code entry."""
        zip_code = convert_to_int(zip_code)
        result = self._filter_data(zip=zip_code)
        return result[0] if result else None

    def get_zipcodes_by_city(self, city):
        """Retrieve zip codes by city."""
        return self._filter_data(primary_city=city)

    def get_zipcodes_by_state(self, state):
        """Retrieve zip codes by state."""
        return self._filter_data(state=state)

    def get_zipcodes_by_city_and_state(self, city, state):
        """Retrieve zip codes by city and state."""
        return self._filter_data(primary_city=city, state=state)

    def get_zipcodes_by_state_and_type(self, state, type_):
        """Retrieve zip codes by state and type."""
        return self._filter_data(state=state, type=type_)

    def get_zipcodes_by_city_and_type(self, city, type_):
        """Retrieve zip codes by city and type."""
        return self._filter_data(primary_city=city, type=type_)

    def get_zipcodes_by_state_city_and_type(self, state, city, type_):
        """Retrieve zip codes by state, city, and type."""
        return self._filter_data(state=state, primary_city=city, type=type_)
