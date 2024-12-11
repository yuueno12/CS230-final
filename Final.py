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
    with certain filtering features 
    that shows the names of the chains and areas. 
    """)
    st.header("About the Dataset")
    st.markdown("""
    The "Fast Food USA" dataset provides geospatial data on fast food restaurants across the states. 
    This information helps visualize what states have what chains of fast food restaurants and vice versa.
    """)

def page2(): #queries and pivot tables
    st.title("Queries and Pivot Tables")
    st.write("This page will display queries and pivot tables.")

def page3():
    st.title("Data Map")
    st.write("This page will display geospatial data on a map.")

def page4():
    st.title("Data Information")
    st.write("This page will provide additional information about the data.")

def main():
    # Ensure the sidebar image is displayed on all pages
    side_bar_image()

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



