import requests


def get_swapi_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def get_planet_name(planet_url):
    planet_data = get_swapi_data(planet_url)
    if planet_data:
        return planet_data['name']
    else:
        return None


def print_film_info(film_id):
    film_data = get_swapi_data(f"https://swapi.dev/api/films/{film_id}/")
