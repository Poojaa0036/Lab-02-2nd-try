# This creates the main landing page for the Streamlit application.
# Contains an introduction to the project and guide users to other pages.


import streamlit as st

st.set_page_config(
    page_title="Homepage",
    page_icon="🏠",
)

st.title("Welcome to the Sports Data Dashboard! 📊")

st.write("""
This application collects and visualizes sports and fitness survey data.

Use the navigation menu on the left to explore the app.

Poojaa Gnanaprakasam

### How to use this app:
- **Survey Page**: Submit your responses to the Sports-Attribute survey.
- **Visuals Page**: Explore graphs and insights generated from both the JSON and CSV datasets.

### About this project
This dashboard examines how different attributes relates to different sports with unique demands.
""")


