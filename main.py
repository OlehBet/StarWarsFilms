import pandas as pd
import requests
import logging
from abc import ABC, abstractmethod

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class SWAPIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def fetch_json(self, endpoint: str) -> list:
        all_data = []
        url = f"{self.base_url}{endpoint}"

        while url:
            logger.info(f"Отримання даних з: {url}")
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            all_data.extend(data['results'])
            url = data.get('next')

        return all_data


class SWAPIDataManager:
    def __init__(self, client: SWAPIClient, filters=None):
        self.client = client
        self.data = {}
        self.filters = filters or []

    def fetch_entity(self, endpoint: str):
        logger.info(f"Завантаження даних для endpoint: {endpoint}")
        self.data[endpoint] = pd.DataFrame(self.client.fetch_json(endpoint))

    def apply_filters(self, endpoint: str):
        if endpoint in self.data:
            logger.info(f"Застосування фільтрів до endpoint: {endpoint}")
            for filter_obj in self.filters:
                filter_obj.apply(self.data[endpoint])
        else:
            logger.warning(f"Дані для endpoint {endpoint} не знайдено.")


class Filter(ABC):
    @abstractmethod
    def apply(self, dataframe: pd.DataFrame):
        pass


class DropColumnsFilter(Filter):
    def __init__(self, columns_to_drop: list):
        self.columns_to_drop = columns_to_drop

    def apply(self, dataframe: pd.DataFrame):
        logger.info(f"Видалення стовпців {self.columns_to_drop}")
        dataframe.drop(columns=self.columns_to_drop, inplace=True)


class ExcelSaver:
    def save_to_excel(self, data: dict, filename: str):
        logger.info(f"Запис даних у Excel файл: {filename}")
        with pd.ExcelWriter(filename) as writer:
            for endpoint, dataframe in data.items():
                sheet_name = endpoint.rstrip('/')
                dataframe.to_excel(writer, sheet_name=sheet_name, index=False)
        logger.info("Дані успішно записано у Excel.")


if __name__ == "__main__":
    client = SWAPIClient(base_url="https://swapi.dev/api/")

    filters = [DropColumnsFilter(columns_to_drop=["films", "species"])]

    manager = SWAPIDataManager(client, filters)

    manager.fetch_entity("people")
    manager.fetch_entity("planets")

    manager.apply_filters("people")

    excel_saver = ExcelSaver()
    excel_saver.save_to_excel(manager.data, "swapi_data.xlsx")
