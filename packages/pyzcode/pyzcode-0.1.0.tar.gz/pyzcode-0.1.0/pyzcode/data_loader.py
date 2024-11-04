import pandas as pd

from .exceptions import DataLoadError


class DataLoader:
    def __init__(self):
        self.data = pd.read_csv("data/zip_code_database.csv").to_dict(
            orient="records"
        )

    def validate_data(self):
        """Validates that data has required columns and is not empty."""
        if not self.data or "zip" not in self.data[0]:
            raise DataLoadError("The data must contain a 'zip' column.")
        if not self.data:
            raise DataLoadError("The data is empty.")
        return True
