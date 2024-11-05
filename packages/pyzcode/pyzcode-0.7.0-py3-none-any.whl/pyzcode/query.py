import random

from .data_loader import DataLoader
from .utils import convert_to_int


class ZipCode:
    def __init__(self, zip_code):
        """
        Initializes a new instance of the class with the given zip code.

        Parameters
        ----------
        zip_code : str
            The zip code to query.

        Raises
        ------
        ValueError
            If no data is found for the given zip code.

        Attributes
        ----------
        zip : str
            The zip code.
        type : str
            The type of the zip code.
        decommissioned : bool
            Whether the zip code is decommissioned.
        primary_city : str
            The primary city for the zip code.
        acceptable_cities : list
            List of acceptable cities for the zip code.
        unacceptable_cities : list
            List of unacceptable cities for the zip code.
        county : str
            The county for the zip code.
        timezone : str
            The timezone for the zip code.
        area_codes : list
            List of area codes for the zip code.
        world_region : str
            The world region for the zip code.
        country : str
            The country for the zip code.
        irs_estimated_population : int
            The IRS estimated population for the zip code.
        """

        query = ZipCodeQuery()
        data = query.get_zipcode(zip_code)
        if data:
            self.zip = data["zip"]
            self.type = data["type"]
            self.decommissioned = data["decommissioned"]
            self.primary_city = data["primary_city"]
            self.state = data["state"]
            self.acceptable_cities = data["acceptable_cities"]
            self.unacceptable_cities = data["unacceptable_cities"]
            self.county = data["county"]
            self.lat = data["latitude"]
            self.lon = data["longitude"]
            self.timezone = data["timezone"]
            self.area_codes = data["area_codes"]
            self.world_region = data["world_region"]
            self.country = data["country"]
            self.irs_estimated_population = data["irs_estimated_population"]
        else:
            raise ValueError(f"No data found for zip code: {zip_code}")

    def __repr__(self):
        """
        Return the dictionary form of the object.

        Returns
        -------
        str
            A string representation of the object's dictionary.
        """

        return str(self.__dict__)


class ZipCodeQuery:
    def __init__(self):
        """
        Initializes the Query class.
        This constructor initializes the Query class by creating an instance
        of the DataLoader classand loading its data into the `data` attribute.
        Attributes
        ----------
        data_loader : DataLoader
            An instance of the DataLoader class used to load data.
        data : Any
            The data loaded by the DataLoader instance.
        """

        self.data_loader = DataLoader()
        self.data = self.data_loader.data

    def _filter_data(self, **kwargs):
        """
        Filters the dataset based on the provided keyword arguments.
        Parameters
        ----------
        **kwargs : dict
            Keyword arguments where the key is the field name and the value is
            the value to filter by.If the value is None, the filter for that
            field is ignored.Special handling is applied for the fields
            "primary_city", "state", and "type" where the comparison is
            case-insensitive.
        Returns
        -------
        list
            A list of dictionaries representing the filtered dataset.
        """

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
        """
        Retrieve data for a given zip code.
        Parameters
        ----------
        zip_code : str or int
            The zip code to query. Can be a string or an integer.
        Returns
        -------
        dict or None
            A dictionary containing the data for the given zip code if found,
            otherwise None.
        """

        zip_code = convert_to_int(zip_code)
        result = self._filter_data(zip=zip_code)
        return result[0] if result else None

    def get_zipcodes_by_city(self, city):
        """
        Get zip codes by city.
        Parameters
        ----------
        city : str
            The name of the city to filter zip codes by.
        Returns
        -------
        list
            A list of zip codes that belong to the specified city.
        """

        return self._filter_data(primary_city=city)

    def get_zipcodes_by_state(self, state):
        """
        Get zip codes by state.
        Parameters
        ----------
        state : str
            The state for which to retrieve zip codes.
        Returns
        -------
        list
            A list of zip codes that belong to the specified state.
        """

        return self._filter_data(state=state)

    def get_zipcodes_by_city_and_state(self, city, state):
        """
        Get zip codes by city and state.
        Parameters
        ----------
        city : str
            The name of the city to filter zip codes by.
        state : str
            The name of the state to filter zip codes by.
        Returns
        -------
        list
            A list of zip codes that match the given city and state.
        """

        return self._filter_data(primary_city=city, state=state)

    def get_zipcodes_by_state_and_type(self, state, type_):
        """
        Get zip codes by state and type.

        Parameters
        ----------
        state : str
            The state for which to filter zip codes.
        type_ : str
            The type of zip codes to filter.

        Returns
        -------
        list
            A list of zip codes that match the given state and type.
        """

        return self._filter_data(state=state, type=type_)

    def get_zipcodes_by_city_and_type(self, city, type_):
        """
        Retrieve zip codes by city and type.

        Parameters
        ----------
        city : str
            The name of the city to filter zip codes by.
        type_ : str
            The type of zip code to filter by.

        Returns
        -------
        list
            A list of zip codes that match the given city and type.
        """

        return self._filter_data(primary_city=city, type=type_)

    def get_zipcodes_by_state_city_and_type(self, state, city, type_):
        """
        Retrieve zip codes based on state, city, and type.
        Parameters
        ----------
        state : str
            The state to filter zip codes by.
        city : str
            The primary city to filter zip codes by.
        type_ : str
            The type of zip code to filter by (e.g., 'STANDARD', 'PO BOX').
        Returns
        -------
        list
            A list of zip codes that match the given state, city, and type.
        """

        return self._filter_data(state=state, primary_city=city, type=type_)

    def random(self):
        """
        Retrieve a random zip code from the dataset.
        Returns
        -------
        dict
            A dictionary representing a random zip code.
        """

        return random.choice(self.data)

    def random_in_state(self, state: str):
        """
        Retrieve a random zip code from the dataset for a given state.
        Parameters
        ----------
        state : str
            The state to filter zip codes by.
        Returns
        -------
        dict
            A dictionary representing a random zip code in the given state.
        """

        return random.choice(self._filter_data(state=state))

    def random_in_city(self, city: str):
        """
        Retrieve a random zip code from the dataset for a given city.
        Parameters
        ----------
        city : str
            The city to filter zip codes by.
        Returns
        -------
        dict
            A dictionary representing a random zip code in the given city.
        """

        return random.choice(self._filter_data(primary_city=city))
