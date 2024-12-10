import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random


# Function to generate random colors for the chart
def generate_random_colors(num_colors):
    return [(random.random(), random.random(), random.random()) for _ in range(num_colors)]


# Caching the data read function for faster loading
@st.cache_data
def read_data():
    df = pd.read_csv("/Users/yuueno/Library/CloudStorage/OneDrive-BentleyUniversity/pythonProject/Final Projects/fast_food_usa.csv")
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
