import streamlit as st
import pandas as pd
import pydeck as pdk

def page3():
    # Function to generate a color map for restaurant names
    def get_color_map(unique_names):
        colors = [
            [255, 0, 0, 160], [0, 255, 0, 160], [0, 0, 255, 160], [255, 255, 0, 160],
            [255, 0, 255, 160], [0, 255, 255, 160], [128, 0, 0, 160], [128, 128, 0, 160],
            [0, 128, 0, 160], [128, 0, 128, 160], [0, 128, 128, 160], [0, 0, 128, 160],
        ]
        # [PY 4] List comprehension that correlates name of chain to color
        color_map = {name: colors[i % len(colors)] for i, name in enumerate(unique_names)}
        return color_map

    # [VIZ 4/MAP] Scatter plot map that allows hovering to show further data
    # [ST 2] Drop down for states/city/chain
    # [DA 5] filter data by two or more conditions (State, city, chain name)
    # color legends for chain names provided
    def show_fast_food_map(data):
        states = data['province'].unique()
        selected_state = st.selectbox("Select a State to Display Fast Food Chains:", ["All"] + sorted(states))
        state_filtered_data = data if selected_state == "All" else data[data['province'] == selected_state]

        # Dropdown to filter by city (based on selected state)
        cities = state_filtered_data['city'].unique()
        selected_city = st.selectbox("Select a City to Filter:", ["All"] + sorted(cities))
        city_filtered_data = state_filtered_data if selected_city == "All" else state_filtered_data[state_filtered_data['city'] == selected_city]

        # Dropdown to filter by chain name
        chains = city_filtered_data['name'].unique()
        selected_chain = st.selectbox("Select a Chain to Filter:", ["All"] + sorted(chains))
        filtered_data = city_filtered_data if selected_chain == "All" else city_filtered_data[city_filtered_data['name'] == selected_chain]

        if not filtered_data.empty:
            unique_chains = sorted(filtered_data['name'].unique())
            color_map = get_color_map(unique_chains)
            filtered_data['color'] = filtered_data['name'].map(color_map)
            # Adjust map view: zoom into city if selected, otherwise use average location
            if selected_city != "All":
                city_lat = filtered_data['latitude'].mean()
                city_lon = filtered_data['longitude'].mean()
                zoom_level = 11  # Closer zoom level for cities
            else:
                city_lat = filtered_data['latitude'].mean()
                city_lon = filtered_data['longitude'].mean()
                zoom_level = 8  # Wider zoom level for states/all data

            view_state = pdk.ViewState(
                latitude=city_lat,
                longitude=city_lon,
                zoom=zoom_level,
                pitch=50,
            )
            # Tooltip = display chain details
            tooltip = {
                "html": "<b>Chain:</b> {name}<br><b>City:</b> {city}<br><b>State:</b> {province}<br><b>Address:</b> {address}",
                "style": {"backgroundColor": "steelblue", "color": "white"},
            }
            # Scatterplot layer with bigger dots
            scatterplot_layer = pdk.Layer(
                "ScatterplotLayer",
                filtered_data,
                get_position=["longitude", "latitude"],
                get_color="color",
                get_radius=1000,  # Increased radius for better visibility
                pickable=True,
            )

            deck = pdk.Deck(
                map_style="mapbox://styles/mapbox/streets-v11",
                initial_view_state=view_state,
                layers=[scatterplot_layer],
                tooltip=tooltip,
            )
            st.pydeck_chart(deck)
            # Display color legend
            st.markdown("### Color Legend for Fast Food Chains")
            for chain, color in color_map.items():
                color_hex = "#{:02x}{:02x}{:02x}".format(color[0], color[1], color[2])
                st.markdown(f"<span style='color:{color_hex};'>●</span> {chain}", unsafe_allow_html=True)
        else:
            st.error("No data available for the selected filters.")

    # Main function for page 3
    def main():
        data = read_data()
        st.title("Fast Food Chains Map Viewer")
        show_fast_food_map(data)

    main()
