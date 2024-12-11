"""
Name:       Yu Ueno
CS230:      Section 7
Data:       Fast food restaurants
Description:    This program provides geospatial data on fast food restaurants across the states.
                This information helps visualize what states have what chains of fast food restaurants and vice versa."""

#Please find the list of requirements at the end of the code for your reference.
#Total counts for requirements [ST: 4, PY: 4, VIZ: 4, DA: 7]

import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import random
import pydeck as pdk

# Function to generate random colors for the chart
def generate_random_colors(num_colors):
    return [(random.random(), random.random(), random.random()) for _ in range(num_colors)]

#allows streamlit to read it faster
@st.cache_data
def read_data():
    df = pd.read_csv("/Users/yuueno/Library/CloudStorage/OneDrive-BentleyUniversity/pythonProject/Final Projects/fast_food_usa.csv")
    df.dropna(subset=['longitude', 'latitude', 'name', 'province', 'city'], inplace=True)
    return df
#[ST 4] image for sidebar
def side_bar_image():
    image_path = "/Users/yuueno/Library/CloudStorage/OneDrive-BentleyUniversity/pythonProject/Final Projects/fast food .jpg"
    if os.path.exists(image_path):
        st.sidebar.image(image_path, use_container_width=True)
    else:
        st.sidebar.warning(f"Image file not found: {image_path}")

def main_page():
    st.title("Fast Food Restaurants in the US")
    st.header("Dataset Overview")
    st.markdown("""
    **Title:** Fast food restaurants  
    **Type:** Geospatial: In the US  
    **Description:** This dataset includes comprehensive information about fast food restaurants across the US,
    with certain filtering features that show the names of the chains and areas. For reference, there was a total of 10,000 entries.
    """)
    st.header("About the Dataset")
    st.markdown("""
    The "Fast Food USA" dataset provides geospatial data on fast food restaurants across the states.
    This information helps visualize what states have what chains of fast food restaurants and vice versa.
    """)

def page2():#queries and pivot tables
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

    # [ST 3] a text box that allows users to enter a State
    # returns a table with a total count of fast food restaurants in selected state
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
            st.write("### Total number of fast food restaurants in state")
            st.table(results_df)
        else:
            st.write("Please enter a state code above.")

    # [PY 2] returns two values based on the top 10 list: total count of a specific chain and the percentage out of the total data entries
    # [DA 3] find top data in a certain column (name/count)
    # [DA 2] Sort data in descending order
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

    # [PY 1] two parameters: dataset and the columns (chains found in waltham)
    # [DA 4] filters data by one condition
    # then filters it out and gives an output of the total count of chains with the expected value across the US
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



def page4():
    # [DA 4] filter data by one condition (state)
    # [VIZ 1] bar charts plotting the number fast food chains by province (state)
    # [PY 2] function that returns more than one value (count and chain name) based on selected state
    def interactive_bar_chart(data, colors):
        # Dropdown to select province (state) sorted alphabetically
        provinces = sorted(data['province'].unique())  # Sort the provinces alphabetically
        # Reference the 'province' column
        selected_province = st.selectbox('Select a Province (State):', provinces)  # Reference the 'province' column
        # Count occurrences of each fast food chain
        filtered_data = data[data['province'] == selected_province]

        chain_counts = filtered_data['name'].value_counts().reset_index()
        chain_counts.columns = ['Chain Name', 'Count']
        chain_counts = chain_counts.sort_values(by='Count', ascending=False)  # Sort in descending order (most to least)
        # Sort in descending order (most to least)
        st.subheader(f'Fast Food Chains in {selected_province}')
        st.markdown("### Bar Chart Showing Count of Fast Food Chains")

        # [DA 2] sort data in descending order
        # Display detailed data in a table
        if not chain_counts.empty:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.bar(chain_counts['Chain Name'], chain_counts['Count'], color=colors[:len(chain_counts)])  # Use the first N colors
            ax.set_ylabel('Count')
            ax.set_xlabel('Chain Name')
            ax.set_title(f'Fast Food Chain Counts in {selected_province}')
            ax.set_xticklabels(chain_counts['Chain Name'], rotation=45, ha='right')
            st.pyplot(fig)
        else:
            st.write(f"No data available for the selected province: {selected_province}")

        if not chain_counts.empty:
            st.write("### Detailed Data Table")
            st.dataframe(chain_counts)
        else:
            st.write("No data to display in the table.")

    # [VIZ 2] Bar chart to display the top 10 fast food chains across the USA
    # [DA 2] sort data in descending order (top 10)
    def top_10_chains_bar_chart(data, colors):
        st.subheader("Top 10 Fast Food Chains in the USA")
        st.markdown("### Bar Chart Showing the Top 10 Chains by Count")

        # Count occurrences of each fast food chain in the entire dataset
        chain_counts = data['name'].value_counts().head(10).reset_index()
        chain_counts.columns = ['Chain Name', 'Count']

        # Generate a bar chart with random colors
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(chain_counts['Chain Name'], chain_counts['Count'], color=colors[:10])
        ax.set_ylabel('Count')
        ax.set_xlabel('Chain Name')
        ax.set_title('Top 10 Fast Food Chains in the USA')
        ax.set_xticklabels(chain_counts['Chain Name'], rotation=45, ha='right')
        st.pyplot(fig)

    # [VIZ 3] interactive bar charts for top states based on selected chains
    # [ST 1] drop down by chains
    def chain_distribution_bar_chart(data, colors):
        st.subheader("Fast Food Chain Distribution by State")
        st.markdown("### Bar Chart Showing Selected Chain's Count Across States")
        # Dropdown to select a chain
        chains = sorted(data['name'].unique())  # Sort the chains alphabetically
        selected_chain = st.selectbox('Select a Chain:', chains)  # Reference the 'name' column
        filtered_data = data[data['name'] == selected_chain]
        # Count occurrences of the selected chain in each state
        state_counts = filtered_data['province'].value_counts().reset_index()
        state_counts.columns = ['State', 'Count']
        state_counts = state_counts.sort_values(by='Count', ascending=False)  # Sort in descending order (most to least)
        # Sort in descending order (most to least)

        # Generate a bar chart with random colors
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(state_counts['State'], state_counts['Count'], color=colors[:len(state_counts)])
        ax.set_ylabel('Count')
        ax.set_xlabel('State')
        ax.set_title(f'{selected_chain} Distribution Across States')
        ax.set_xticklabels(state_counts['State'], rotation=45, ha='right')
        st.pyplot(fig)

    def main():
        data = read_data()

        # Generate color palettes once
        all_chains = data['name'].unique()
        all_states = data['province'].unique()
        all_colors = generate_random_colors(max(len(all_chains), len(all_states)))

        interactive_bar_chart(data, all_colors)
        top_10_chains_bar_chart(data, all_colors)
        chain_distribution_bar_chart(data, all_colors)

    main()

# Sidebar navigation
def main():
    st.sidebar.title("Navigation")
    side_bar_image()
    #page directory alongside image
    pages_dict = {
        "Home": main_page,
        "Queries and Pivot Tables": page2,
        "Scatter Plot Map": page3,
        "Data Information": page4
    }
    selected_page = st.sidebar.radio("Select a page:", list(pages_dict.keys()))

    # Call the app function based on selection
    pages_dict[selected_page]()

if __name__ == "__main__":
    main()

#Summary of requirements for final project
#ST 4 = sidebar image
#ST 3 = text box for state
#PY 2= returns 2 values of top ten
#DA 3= top 10 (find top data in certain column)
#DA 2 = sort data in descending order
#PY 1= two parameters (waltham, count)
#DA 4 = filters data by one condition (in waltham)
#PY 4 = list comprehension (name of chain & color)
#[VIZ 4/MAP] = scatter plot map that allows hovering to show further data
#ST 2 = drop down for states
#DA 5 = filter data by two or more (state, city, chain name) in maps
#DA 4= filter data by one condition (state)
#VIZ 1 = bar charts with count of fast food chains by selected state
#PY 2= function that returns more than one value (count and chain name)
#DA 2 = sort data in descending order based from selected state
#VIZ 2 = bar charts to show top 10 fast food restaurants by count
#DA 2=  sort data in descending order by total count (top 10)
#VIZ 3 = bar charts for top states based on selected chains
#ST 1 = drop down by chains
#Total counts for requirements [ST: 4, PY: 4, VIZ: 4, DA: 7]
