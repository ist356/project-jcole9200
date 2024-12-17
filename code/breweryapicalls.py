
import requests

base_url = "https://api.openbrewerydb.org/v1/breweries"

def get_brewery_details(brewery_id: str) -> dict:
    url = f"{base_url}/{brewery_id}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def get_breweries_by_city(city: str) -> list:
    params = { "by_city": city }
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    return response.json()


def get_breweries_by_state(state: str) -> list:
    params = { "by_state": state }
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    return response.json()


def get_breweries_by_type(brewery_type: str) -> list:
    params = { "by_type": brewery_type }
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    return response.json()


def search_breweries(query: str) -> list:
    params = { "query": query }
    url = f"{base_url}/search"
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def autocomplete_breweries(query: str) -> list:
    params = { "query": query }
    url = f"{base_url}/autocomplete"
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def get_random_brewery() -> dict:
    url = f"{base_url}/random"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":

    random_brewery = get_random_brewery()
    print("Random Brewery:", random_brewery)

    city_breweries = get_breweries_by_city("San Diego")
    print(f"Breweries in San Diego: {len(city_breweries)} found.")

    suggestions = autocomplete_breweries("Stone")
    print("Autocomplete suggestions:", suggestions)

    if city_breweries:
        brewery_id = city_breweries[0]["id"]
        brewery_details = get_brewery_details(brewery_id)
        print("Brewery Details:", brewery_details)
