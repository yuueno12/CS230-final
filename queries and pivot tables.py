import streamlit as st
import pandas as pd
import os

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
