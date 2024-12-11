import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random

# Function to generate random colors for the chart
#move to top in final.py
def generate_random_colors(num_colors):
    return [(random.random(), random.random(), random.random()) for _ in range(num_colors)]

#allows streamlit to read it faster
#move to top in final.py
@st.cache_data
def read_data():
    df = pd.read_csv("/Users/yuueno/Library/CloudStorage/OneDrive-BentleyUniversity/pythonProject/Final Projects/fast_food_usa.csv")
    df.dropna(subset=['longitude', 'latitude', 'name', 'province', 'city'], inplace=True)
    return df


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

