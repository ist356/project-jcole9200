
import pytest
import pandas as pd
import streamlit as st
import requests

from code.brewerylocator import (
    save_to_cache,
    load_from_cache,
    create_map,
    cache_file
)

def test_save_to_cache():
    test_data = pd.DataFrame({
        'name': ['Brewery 1', 'Brewery 2'],
        'city': ['San Diego', 'San Diego'],
        'state': ['California', 'California'],
        'brewery_type': ['micro', 'brewpub'],
        'latitude': [32.7157, 32.7158],
        'longitude': [-117.1611, -117.1612]
    })
    save_to_cache(test_data, cache_file)
    df = pd.read_csv(cache_file)
    assert df.shape[0] == test_data.shape[0]
    assert df.shape[1] == test_data.shape[1]


def test_load_from_cache():
    test_data = pd.DataFrame({
        'name': ['Brewery 1', 'Brewery 2'],
        'city': ['San Diego', 'San Diego'],
        'state': ['California', 'California'],
        'brewery_type': ['micro', 'brewpub'],
        'latitude': [32.7157, 32.7158],
        'longitude': [-117.1611, -117.1612]
    })
    save_to_cache(test_data, cache_file)
    df = load_from_cache(cache_file)
    assert df is not None
    assert df.shape[0] == test_data.shape[0]
    assert df.shape[1] == test_data.shape[1]


def test_create_map_valid_data():
    breweries_df = pd.DataFrame({
        'name': ['Brewery 1', 'Brewery 2'],
        'city': ['San Diego', 'San Diego'],
        'state': ['California', 'California'],
        'brewery_type': ['micro', 'brewpub'],
        'latitude': [32.7157, 32.7158],
        'longitude': [-117.1611, -117.1612]
    })

    brewery_map = create_map(breweries_df)
    assert brewery_map is not None 


def test_create_map_invalid_data():
    breweries_df = pd.DataFrame({
        'name': ['Brewery 1', 'Brewery 2'],
        'city': ['San Diego', 'San Diego'],
        'state': ['California', 'California'],
        'brewery_type': ['micro', 'brewpub'],
        'latitude': [None, None],
        'longitude': [None, None]
    })
    brewery_map = create_map(breweries_df)
    assert brewery_map is None


if __name__ == "__main__":
    pytest.main()
