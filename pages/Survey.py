import streamlit as st
import csv
import os
import pandas as pd
from pathlib import Path

CSV_PATH = Path(__file__).parent.parent / "data.csv"

COLUMNS = [
    "name",
    "most_interesting_sport",
    "physical_activity",
    "plays_competitively",
    "strongest_attribute",
    "years_playing"
]

st.title("Data Collection Survey 📝")

st.write(
    "Please fill out this self-reflective survey to contribute to our dataset!"
)

with st.form("survey_form"):

    name = st.text_input(
        "What's your name (just first name is enough)?"
    )

    most_interesting_sport = st.selectbox(
        "Regardless of whether you are an athlete or not, which sport interests you the most?",
        [
            "Soccer",
            "Swimming",
            "Gymnastics",
            "Basketball",
            "Weightlifting",
            "Dance",
            "Volleyball",
            "Other"
        ]
    )

    physical_activity = st.slider(
        "About how many hours per week do you engage in physical activity?",
        0,
        30,
        5
    )

    plays_competitively = st.radio(
        "Do you play competitively?",
        ["Yes", "No"]
    )

    strongest = st.multiselect(
        "Out of the following sports attributes, which ones do you believe you are the strongest at? (pick up to 3)",
        [
            "Endurance",
            "Strength",
            "Speed",
            "Agility",
            "Flexibility",
            "Balance & coordination",
            "Body composition"
        ],
        max_selections=3
    )

    years_playing = st.number_input(
        "How many years have you played your main sport?",
        min_value=0,
        max_value=50,
        value=1,
        step=1
    )

    submitted = st.form_submit_button("Submit")

    if submitted:

        if name.strip() == "":
            st.warning("Please enter a name.")

        elif len(strongest) == 0:
            st.warning("Please select at least one attribute.")

        else:

            file_is_empty = (
                not CSV_PATH.exists()
                or os.path.getsize(CSV_PATH) == 0
            )

            with open(CSV_PATH, "a", newline="") as f:

                writer = csv.writer(f)

                if file_is_empty:
                    writer.writerow(COLUMNS)

                writer.writerow([
                    name.strip(),
                    most_interesting_sport,
                    physical_activity,
                    plays_competitively,
                    ";".join(strongest),
                    years_playing
                ])

            st.success(
                "Thank you for your response! Hope you enjoyed the survey."
            )

st.divider()

st.header("Current Data in CSV")

if CSV_PATH.exists() and os.path.getsize(CSV_PATH) > 0:

    current_data_df = pd.read_csv(CSV_PATH)

    st.dataframe(current_data_df)

else:

    st.warning(
        "The data.csv file is empty or does not exist yet."
    )
