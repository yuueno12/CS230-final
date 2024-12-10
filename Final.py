"""
Name:       Yu Ueno
CS230:      Section 7
Data:       Fast food restaurants
Description:    This program ... (a few sentences about your program and the queries and charts)"""

import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import random

def main_page():
    def side_bar_image():
        image_path = "fast food.jpg"
        if os.path.exists(image_path):
            st.sidebar.image(image_path, use_column_width=True)
        else:
            st.sidebar.warning(f"Image file not found: {image_path}")

    def data_source_page():
        st.title("Fast Food Restaurants in the US")
        st.header("Dataset Overview")
        st.markdown("""
        **Title:** Fast food restaurants  
        **Type:** Geospatial: In the US  
        **Description:** This dataset includes comprehensive information about fast food restaurants across the US, 
        with certain filtering features 
        that shows the names of the chains and areas. 
        """)
        st.header("About the Dataset")
        st.markdown("""
        The "Fast Food USA" dataset provides geospatial data on fast food restaurants across the states. 
        This information helps visualize what states have what chains of fast food restaurants and vice versa.
        """)

    def run():
        side_bar_image()
        data_source_page()

    run()

import streamlit as st
import pandas as pd
import os

def main_page():
    def side_bar_image():
        image_path = "fast food.jpg"
        if os.path.exists(image_path):
            st.sidebar.image(image_path, use_column_width=True)
        else:
            st.sidebar.warning(f"Image file not found: {image_path}")

    def data_source_page():
        st.title("Fast Food Restaurants in the US")
        st.header("Dataset Overview")
        st.markdown("""
        **Title:** Fast food restaurants  
        **Type:** Geospatial: In the US  
        **Description:** This dataset includes comprehensive information about fast food restaurants across the US, 
        with certain filtering features 
        that shows the names of the chains and areas. 
        """)
        st.header("About the Dataset")
        st.markdown("""
        The "Fast Food USA" dataset provides geospatial data on fast food restaurants across the states. 
        This information helps visualize what states have what chains of fast food restaurants and vice versa.
        """)

    def run():
        side_bar_image()
        data_source_page()

    run()

def page2():
    @st.cache_data
    def load_data():
        path = "/Users/yuueno/Library/CloudStorage/OneDrive-BentleyUniversity/pythonProject/Final Projects/fast_food_usa.csv"
        if os.path.exists(path):
            df = pd.read_csv(path)
            df['province'] = df['province'].str.lower()
            if df.empty:
                st.error("Loaded data is empty.")
            return df
        else:
            st.error(f"CSV file not found at: {path}")
            return pd.DataFrame()  # Return an empty DataFrame

    def State_text_box():
        st.title("Fast food chains by state")
        df = load_data()
        province_name = st.text_input("Enter a state code (e.g., MA, NY, TX):").lower().strip()
        if province_name:
            count = df[df['province'] == province_name].shape[0]
            results_df = pd.DataFrame({
                'State Code': [province_name.upper()],
                'Total Count': [count]
            })
            st.write("### Total number of fast food restaurant in state")
            st.table(results_df)
        else:
            st.write("Please enter a state code above.")

    def chain_counts():
        df = load_data()
        if df.empty:
            return None, None
        if "name" not in df.columns:
            st.error("The expected column 'name' is not found in the dataset.")
            return None, None
        top_10_names = df["name"].value_counts().head(10)
        total = df["name"].value_counts().sum()
        results_df = pd.DataFrame({
            "Name of chain": top_10_names.index,
            'Total Count': top_10_names.values,
            'Percentage': ((top_10_names / total) * 100).round(2).astype(str) + '%'
        })
        return results_df, total

    def display_names():
        results_df, total = chain_counts()
        if results_df is not None and total is not None:
            st.write(
                '<style>thead th {text-align: center;} tbody td {text-align: left;} th, td {font-size: 18px;}</style>',
                unsafe_allow_html=True)
            st.write("### Top 10 Chains")
            st.write(f"Total number of restaurants: {total}")
            st.dataframe(results_df)
        else:
            st.write("No data to display.")

    def waltham_chains(data, column_name="name"):
        if data.empty:
            return
        if column_name not in data.columns:
            st.error(f"The column '{column_name}' does not exist in the dataset.")
            return None
        # Filter data to only include expected categories
        expected_categories = ["McDonald's", "Wendy's", "Dunkin' Donuts", "Chipotle Mexican Grill", "Five Guys", "Panera Bread", "Starbucks Coffee"]
        filtered_data = data[data[column_name].isin(expected_categories)]
        waltham_counts = filtered_data[column_name].value_counts()
        results_df = pd.DataFrame({
            'Category': waltham_counts.index,
            'Total Count': waltham_counts.values
        })
        # Ensure all expected categories are included
        for category in expected_categories:
            if category not in results_df['Category'].tolist():
                results_df = pd.concat([results_df, pd.DataFrame({'Category': [category], 'Total Count': [0]})], ignore_index=True)
        st.write("### Chains found in Waltham")
        st.table(results_df)

    def run():
        State_text_box()
        display_names()
        waltham_chains(data=load_data())

    run()

# Assuming you have a Streamlit multipage setup, you would call the pages like this:
main_page()
page2()





def page3():
    # Load the data
    file_path = '/Users/yuueno/Library/CloudStorage/OneDrive-BentleyUniversity/pythonProject/Final Projects/fast_food_usa.csv'

    @st.cache_data
    def read_data():
        df = pd.read_csv(file_path)
        df.dropna(subset=['longitude', 'latitude', 'name', 'province', 'city'], inplace=True)
        return df

    # Function to generate a color map for restaurant names
    def get_color_map(unique_names):
        colors = [
            [255, 0, 0, 160], [0, 255, 0, 160], [0, 0, 255, 160], [255, 255, 0, 160],
            [255, 0, 255, 160], [0, 255, 255, 160], [128, 0, 0, 160], [128, 128, 0, 160],
            [0, 128, 0, 160], [128, 0, 128, 160], [0, 128, 128, 160], [0, 0, 128, 160],
        ]
        color_map = {name: colors[i % len(colors)] for i, name in enumerate(unique_names)}
        return color_map

    # Map display logic
    def show_fast_food_map(data):
        # Dropdown to filter by state
        states = data['province'].unique()
        selected_state = st.selectbox("Select a State to Display Fast Food Chains:", ["All"] + sorted(states))
        state_filtered_data = data if selected_state == "All" else data[data['province'] == selected_state]

        # Dropdown to filter by city (based on selected state)
        cities = state_filtered_data['city'].unique()
        selected_city = st.selectbox("Select a City to Filter:", ["All"] + sorted(cities))
        city_filtered_data = state_filtered_data if selected_city == "All" else state_filtered_data[
            state_filtered_data['city'] == selected_city]

        # Dropdown to filter by chain name
        chains = city_filtered_data['name'].unique()
        selected_chain = st.selectbox("Select a Chain to Filter:", ["All"] + sorted(chains))
        filtered_data = city_filtered_data if selected_chain == "All" else city_filtered_data[
            city_filtered_data['name'] == selected_chain]

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

            # Tooltip to display chain details
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

    # Main function
    def main():
        data = read_data()
        st.title("Fast Food Chains Map Viewer")
        show_fast_food_map(data)

    main()
    return
def page4():
    # Function to generate random colors for the chart
    def generate_random_colors(num_colors):
        return [(random.random(), random.random(), random.random()) for _ in range(num_colors)]

    # Caching the data read function for faster loading
    @st.cache_data
    def read_data():
        df = pd.read_csv(
            "/Users/yuueno/Library/CloudStorage/OneDrive-BentleyUniversity/pythonProject/Final Projects/fast_food_usa.csv")
        return df

    # Plotting the bar chart of fast food chains by province (state)
    def interactive_bar_chart(data):
        # Dropdown to select province (state) sorted alphabetically
        provinces = sorted(data['province'].unique())  # Sort the provinces alphabetically
        selected_province = st.selectbox('Select a Province (State):', provinces)  # Reference the 'province' column
        filtered_data = data[data['province'] == selected_province]

        # Count occurrences of each fast food chain
        chain_counts = filtered_data['name'].value_counts().reset_index()
        chain_counts.columns = ['Chain Name', 'Count']
        chain_counts = chain_counts.sort_values(by='Count', ascending=False)  # Sort in descending order (most to least)

        st.subheader(f'Fast Food Chains in {selected_province}')
        st.markdown("### Bar Chart Showing Count of Fast Food Chains")

        # Generate a bar chart with random colors
        if not chain_counts.empty:
            fig, ax = plt.subplots(figsize=(10, 6))
            colors = generate_random_colors(len(chain_counts))
            ax.bar(chain_counts['Chain Name'], chain_counts['Count'], color=colors)
            ax.set_ylabel('Count')
            ax.set_xlabel('Chain Name')
            ax.set_title(f'Fast Food Chain Counts in {selected_province}')
            ax.set_xticklabels(chain_counts['Chain Name'], rotation=45, ha='right')
            st.pyplot(fig)
        else:
            st.write(f"No data available for the selected province: {selected_province}")

        # Display detailed data in a table
        if not chain_counts.empty:
            st.write("### Detailed Data Table")
            st.dataframe(chain_counts)
        else:
            st.write("No data to display in the table.")

    def main():
        st.title('Fast Food Chains in the USA')

        # Load the data
        data = read_data()

        # Call the interactive bar chart function
        interactive_bar_chart(data)

    main()

def main():
    pages_dict = {
        "Home": main_page,
        "Queries and Pivot Tables": page2,
        "Data Map": page3,
        "Data Information": page4
    }
    selected_page = st.sidebar.radio("Select a page:", list(pages_dict.keys()))

    # Call the app function based on selection
    pages_dict[selected_page]()

main()


