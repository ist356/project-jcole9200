import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
import requests

from breweryapicalls import (
    get_breweries_by_city,
    get_breweries_by_state,
    get_breweries_by_type,
    autocomplete_breweries,
    get_random_brewery,
)

cache_file = "cache/breweries.csv"

def save_to_cache(data: pd.DataFrame, filename: str):
    data.to_csv(filename, index=False)

def load_from_cache(filename: str) -> pd.DataFrame | None:
    try:
        return pd.read_csv(filename)
    except FileNotFoundError:
        return None

def create_map(breweries_df: pd.DataFrame) -> folium.Map:
    breweries_df = breweries_df.dropna(subset=['latitude', 'longitude'])
    if breweries_df.empty:
        st.write("No valid breweries with coordinates to display on the map.")
        return None

    map_center = [breweries_df['latitude'].iloc[0], breweries_df['longitude'].iloc[0]]
    brewery_map = folium.Map(location=map_center, zoom_start=12)
    marker_cluster = MarkerCluster().add_to(brewery_map)

    for _, brewery in breweries_df.iterrows():
        popup_content = f"""
        <b>{brewery['name']}</b><br>
        Type: {brewery['brewery_type']}<br>
        Location: {brewery['city']}, {brewery['state']}<br>
        Coordinates: ({brewery['latitude']}, {brewery['longitude']})
        """
        folium.Marker(
            location=[brewery['latitude'], brewery['longitude']],
            popup=folium.Popup(popup_content, max_width=300)
        ).add_to(marker_cluster)

    return brewery_map

def main():
    st.title("Brewery Finder")

    st.sidebar.header("Search for Breweries")
    city = st.sidebar.text_input("City")
    state = st.sidebar.text_input("State")
    brewery_type = st.sidebar.selectbox("Brewery Type", ["micro", "brewpub", "regional", "large", "contract", "planning", "proprietor", "closed", ""])
    search_button = st.sidebar.button("Search")

    st.sidebar.header("Enter a Keyword for Brewery Search")
    brewery_name_query = st.sidebar.text_input("Brewery Name Query")
    autocomplete_button = st.sidebar.button("Search by Keyword")

    st.sidebar.header("Recommendation")
    random_button = st.sidebar.button("Surprise Me!")

    if search_button:
        st.subheader("Search Results")
        if city or state or brewery_type:
            breweries = []
            if city:
                breweries += get_breweries_by_city(city)
            if state:
                breweries += get_breweries_by_state(state)
            if brewery_type:
                breweries = [b for b in breweries if b["brewery_type"] == brewery_type]

            if breweries:
                breweries_df = pd.DataFrame(breweries)
                st.write(breweries_df)
                save_to_cache(breweries_df, cache_file)
                
                if 'latitude' in breweries_df.columns and 'longitude' in breweries_df.columns:
                    brewery_map = create_map(breweries_df)
                    if brewery_map:  # Only display the map if valid data is present
                        folium_static(brewery_map)
                else:
                    st.write("No geographical data available for mapping.")
            else:
                st.write("No breweries found.")
        else:
            st.write("Please enter at least one search criteria.")

    if autocomplete_button:
        st.subheader("Autocomplete Results")
        if brewery_name_query:
            suggestions = autocomplete_breweries(brewery_name_query)
            if suggestions:
                st.write(pd.DataFrame(suggestions))
            else:
                st.write("No autocomplete suggestions found.")
        else:
            st.write("Please enter a query to get suggestions.")

    if random_button:
        st.subheader("Random Brewery Recommendation")
        random_brewery = get_random_brewery()
        if random_brewery:
            st.write(pd.DataFrame([random_brewery]))
        else:
            st.write("No brewery found.")


if __name__ == "__main__":
    main()
