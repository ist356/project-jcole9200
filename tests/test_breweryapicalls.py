
import pytest
import requests

from code.breweryapicalls import (
    get_brewery_details,
    get_breweries_by_city,
    get_breweries_by_state,
    get_breweries_by_type,
    autocomplete_breweries,
    get_random_brewery,
)


def test_get_brewery_details():
    test_brewery_id = "1"
    expected_name = "Buried Acorn Brewery" 
    brewery_details = get_brewery_details(test_brewery_id)
    assert brewery_details["name"] == expected_name


def test_get_breweries_by_city():
    city = "San Diego"
    breweries = get_breweries_by_city(city)
    assert isinstance(breweries, list)
    assert all("name" in b for b in breweries)
    assert all("city" in b for b in breweries)
    assert all(b["city"] == city for b in breweries)


def test_get_breweries_by_state():
    state = "California"
    breweries = get_breweries_by_state(state)
    assert isinstance(breweries, list)
    assert all("name" in b for b in breweries)
    assert all("state" in b for b in breweries)
    assert all(b["state"] == state for b in breweries)


def test_get_breweries_by_type():
    brewery_type = "micro"
    breweries = get_breweries_by_type(brewery_type)
    assert isinstance(breweries, list)
    assert all("name" in b for b in breweries)
    assert all("brewery_type" in b for b in breweries)
    assert all(b["brewery_type"] == brewery_type for b in breweries)


def test_autocomplete_breweries():
    query = "Stone"
    suggestions = autocomplete_breweries(query)
    assert isinstance(suggestions, list)
    assert all("name" in suggestion for suggestion in suggestions)


def test_get_random_brewery():
    random_brewery = get_random_brewery()
    assert "id" in random_brewery


if __name__ == "__main__":
    pytest.main()
