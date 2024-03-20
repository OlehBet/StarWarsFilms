import requests


def get_swapi_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None
