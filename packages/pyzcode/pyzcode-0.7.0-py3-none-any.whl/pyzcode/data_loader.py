import pandas as pd

from .exceptions import DataLoadError


class DataLoader:
    def __init__(self):
        """
        Initializes the DataLoader object by reading data from a CSV file and
        converting it to a list of dictionaries.
        Attributes
        ----------
        data : list of dict
            A list of dictionaries where each dictionary represents a record
            from the CSV file.
        """

        self.data = pd.read_csv("pyzcode/data/zip_code_database.csv").to_dict(
            orient="records"
        )

    def validate_data(self):
        """
        Validates the data to ensure it meets the required criteria.

        Raises
        ------
        DataLoadError
            If the data does not contain a 'zip' column.
            If the data is empty.

        Returns
        -------
        bool
            True if the data is valid.
        """

        if not self.data or "zip" not in self.data[0]:
            raise DataLoadError("The data must contain a 'zip' column.")
        if not self.data:
            raise DataLoadError("The data is empty.")
        return True
