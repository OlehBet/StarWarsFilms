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
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            all_data.extend(data['results'])
            url = data.get('next')

        return all_data

class EntityProcessor(ABC):
    @abstractmethod
    def process(self, json_data: list) -> pd.DataFrame:
        pass

class PeopleProcessor(EntityProcessor):
    def process(self, json_data: list) -> pd.DataFrame:
        df = pd.DataFrame(json_data)
        df['full_name'] = df['name']
        return df

class PlanetsProcessor(EntityProcessor):
    def process(self, json_data: list) -> pd.DataFrame:
        df = pd.DataFrame(json_data)
        df['population'] = pd.to_numeric(df['population'], errors='coerce')
        return df

class SWAPIDataManager:
    def __init__(self, client: SWAPIClient):
        self.client = client
        self.data = {}
        self.processors = {}

    def register_processor(self, endpoint: str, processor: EntityProcessor):
        self.processors[endpoint] = processor

    def fetch_entity(self, endpoint: str):
        logger.info(f"Завантаження даних для endpoint: {endpoint}")
        raw_data = self.client.fetch_json(endpoint)
        if endpoint in self.processors:
            processor = self.processors[endpoint]
            self.data[endpoint] = processor.process(raw_data)
        else:
            logger.warning(f"Обробник для {endpoint} не знайдений.")

    def save_to_excel(self, filename: str):
        logger.info(f"Запис даних у Excel файл: {filename}")
        with pd.ExcelWriter(filename) as writer:
            for endpoint, dataframe in self.data.items():
                sheet_name = endpoint.rstrip('/')
                dataframe.to_excel(writer, sheet_name=sheet_name, index=False)
        logger.info("Дані успішно записано у Excel.")

if __name__ == "__main__":
    client = SWAPIClient(base_url="https://swapi.dev/api/")
    manager = SWAPIDataManager(client)

    manager.register_processor("people", PeopleProcessor())
    manager.register_processor("planets", PlanetsProcessor())

    manager.fetch_entity("people")
    manager.fetch_entity("planets")

    manager.save_to_excel("swapi_data.xlsx")
