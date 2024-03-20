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
    if film_data:
        print("Фільм:", film_data['title'])
        print("Персонажі:")
        for character_url in film_data['characters']:
            character_data = get_swapi_data(character_url)
            if character_data:
                print(f"  {character_data['name']} з планети {get_planet_name(character_data['homeworld'])}")
        print("Транспорті засоби:")
        for vehicle_url in film_data['vehicles']:
            vehicle_data = get_swapi_data(vehicle_url)
            if vehicle_data:
                print(f"  {vehicle_data['name']}")
        print("Космічні кораблі:")
        for starship_url in film_data['starships']:
            starship_data = get_swapi_data(starship_url)
            if starship_data:
                print(f"  {starship_data['name']}")
        print("Види істот:")
        for species_url in film_data['species']:
            species_data = get_swapi_data(species_url)
            if species_data:
                print(f"  {species_data['name']}")
    else:
        print("Фільм не знайдено.")


if __name__ == "__main__":
    film_id = input("Введіть ідентефікатор фільму: ")
    print_film_info(film_id)
