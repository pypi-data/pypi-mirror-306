class ZipCodeNotFoundError(Exception):
    """Raised when a zipcode is not found in the database"""

    pass


class DataLoadError(Exception):
    """Raised when there is an error loading the data"""

    pass
