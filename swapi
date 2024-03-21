from swapi import get_film


def get_film_info():
    film = get_film(1)
    characters = film.get_characters().items
    vehicles = film.get_vehicles().items
    starships = film.get_starships().items
    species = film.get_species().items

    print(f"Фільм: {film.title}")

    print("Персонажі: ")
    for index, character in enumerate(characters, 1):
        print(f"{index} {character.name} з планети ({character.get_homeworld().name})")

    print("Транспортні засоби: ")
    for index, vehicle in enumerate(vehicles, 1):
        print(f"{index} {vehicle.name}")

    print("Космічні кораблі: ")
    for index, starship in enumerate(starships, 1):
        print(f"{index} {starship.name}")

    print("Види істот: ")
    for index, specie in enumerate(species, 1):
        print(f"{index} {specie.name}")


if __name__ == "__main__":
    film_id = input("Введіть ідентифікатор фільму: ")
    get_film_info()
