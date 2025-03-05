import logging

import pandas as pd
import requests

from functions.interfaces import DataProviderInterface

logger = logging.getLogger(__name__)


class SWAPIClient(DataProviderInterface):
    def __init__(self, path: str):
        self.base_url = path

    def fetch_data(self, endpoint: str):
        all_data = []
        url = f"{self.base_url}{endpoint}"

        while url:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            all_data.extend(data['results'])
            url = data.get('next')

        return all_data


class ExcelSWAPIClient(DataProviderInterface):
    def __init__(self, path: str):
        self.path = path
        self.data = pd.read_excel(path, sheet_name=None)

    def fetch_data(self, endpoint: str):
        if endpoint not in self.data:
            logger.warning(f"Кінцеву точку {endpoint} не знайдено в {self.path}")
            return []
        return self.data[endpoint].to_dict(orient='records')
