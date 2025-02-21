import pandas as pd
import requests
import logging
import argparse
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


class ExcelSWAPIClient:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def fetch_json(self, endpoint: str) -> list:
        df = pd.read_excel(self.file_path, sheet_name=endpoint)
        return df.to_dict(orient='records')


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
    def __init__(self, client):
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


def main():
    parser = argparse.ArgumentParser(description="SWAPI Data Manager")
    parser.add_argument('--input', required=True, help="URL або шлях до .xlsx файлу")
    parser.add_argument('--endpoint', required=True, help="Кома розділені імена endpoint-ів (наприклад, 'people,planets')")
    parser.add_argument('--output', required=True, help="Шлях до файлу для збереження результатів")

    args = parser.parse_args()

    if args.input.startswith('http'):
        client = SWAPIClient(base_url=args.input)
    else:
        client = ExcelSWAPIClient(file_path=args.input)

    manager = SWAPIDataManager(client)

    endpoints = args.endpoint.split(',')
    manager.register_processor("people", PeopleProcessor())
    manager.register_processor("planets", PlanetsProcessor())

    for endpoint in endpoints:
        manager.fetch_entity(endpoint)

    manager.save_to_excel(args.output)


if __name__ == "__main__":
    main()

