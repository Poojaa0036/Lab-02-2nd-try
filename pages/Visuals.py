import streamlit as st
import json
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Visuals",
    page_icon="📈"
)

st.title("Data Visualizations 📈")

# ----------------------------
# LOAD JSON DATA
# ----------------------------

JSON_PATH = Path(__file__).parent.parent / "data.json"

with open(JSON_PATH) as f:
    data = json.load(f)

chart_title = data.get("chart_title", "Sports Attributes")
data.pop("chart_title", None)

df = pd.DataFrame(data).T.astype(float)

# ----------------------------
# JSON STATIC VISUALIZATION
# ----------------------------

st.header("JSON Visualizations")

st.subheader("Average Fitness Score by Sport")

avg_scores = df.mean(axis=1)

fig, ax = plt.subplots()

ax.bar(avg_scores.index, avg_scores.values)

ax.set_title("Average Fitness Score by Sport")
ax.set_xlabel("Sport")
ax.set_ylabel("Average Fitness Score")

plt.xticks(rotation=45)

st.pyplot(fig)

# ----------------------------
# JSON DYNAMIC VISUALIZATION
# ----------------------------

st.subheader("Compare Sport Attributes")

attributes = list(df.columns)

if "x_attr" not in st.session_state:
    st.session_state.x_attr = attributes[0]

if "y_attr" not in st.session_state:
    st.session_state.y_attr = attributes[1]

st.selectbox(
    "Choose X-axis attribute",
    attributes,
    key="x_attr"
)

st.selectbox(
    "Choose Y-axis attribute",
    attributes,
    key="y_attr"
)

fig2 = px.scatter(
    df,
    x=st.session_state.x_attr,
    y=st.session_state.y_attr,
    text=df.index,
    title=f"{st.session_state.y_attr} vs {st.session_state.x_attr}"
)

fig2.update_traces(
    textposition="top center"
)

st.plotly_chart(fig2)

stats = {
    "x_mean": df[st.session_state.x_attr].mean(),
    "x_median": df[st.session_state.x_attr].median(),
    "y_mean": df[st.session_state.y_attr].mean(),
    "y_median": df[st.session_state.y_attr].median()
}

selection = (
    st.session_state.x_attr,
    st.session_state.y_attr
)

if "last_selection" not in st.session_state:

    st.session_state.last_selection = selection
    st.session_state.curr_stats = stats
    st.session_state.prev_stats = stats

elif selection != st.session_state.last_selection:

    st.session_state.prev_stats = st.session_state.curr_stats
    st.session_state.curr_stats = stats
    st.session_state.last_selection = selection

curr = st.session_state.curr_stats
prev = st.session_state.prev_stats

st.subheader("Summary Statistics")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    f"{st.session_state.x_attr} Mean",
    round(curr["x_mean"], 2),
    round(curr["x_mean"] - prev["x_mean"], 2)
)

col2.metric(
    f"{st.session_state.x_attr} Median",
    round(curr["x_median"], 2),
    round(curr["x_median"] - prev["x_median"], 2)
)

col3.metric(
    f"{st.session_state.y_attr} Mean",
    round(curr["y_mean"], 2),
    round(curr["y_mean"] - prev["y_mean"], 2)
)

col4.metric(
    f"{st.session_state.y_attr} Median",
    round(curr["y_median"], 2),
    round(curr["y_median"] - prev["y_median"], 2)
)

# ----------------------------
# CSV DATA
# ----------------------------

CSV_PATH = Path(__file__).parent.parent / "data.csv"

csv_df = pd.read_csv(CSV_PATH)

st.header("CSV Visualizations")

# ----------------------------
# CSV STATIC VISUALIZATION
# ----------------------------

st.subheader("Most Interesting Sports")

sport_counts = csv_df[
    "most_interesting_sport"
].value_counts()

fig3, ax3 = plt.subplots()

ax3.bar(
    sport_counts.index,
    sport_counts.values
)

ax3.set_title("Favorite Sports")
ax3.set_xlabel("Sport")
ax3.set_ylabel("Number of Responses")

plt.xticks(rotation=45)

st.pyplot(fig3)

# ----------------------------
# CSV DYNAMIC VISUALIZATION
# ----------------------------

st.subheader("Physical Activity by Experience")

if "minimum_years" not in st.session_state:
    st.session_state.minimum_years = 0

st.slider(
    "Minimum Years Playing",
    0,
    int(csv_df["years_playing"].max()),
    key="minimum_years"
)

filtered_df = csv_df[
    csv_df["years_playing"]
    >= st.session_state.minimum_years
]

fig4 = px.scatter(
    filtered_df,
    x="years_playing",
    y="physical_activity",
    color="most_interesting_sport",
    hover_name="name",
    title="Years Playing vs Physical Activity"
)

fig4.update_layout(
    xaxis_title="Years Playing",
    yaxis_title="Hours of Physical Activity Per Week"
)

st.plotly_chart(fig4)

st.subheader("Filtered Statistics")

mean_activity = filtered_df[
    "physical_activity"
].mean()

median_activity = filtered_df[
    "physical_activity"
].median()

c1, c2 = st.columns(2)

c1.metric(
    "Mean Activity Hours",
    round(mean_activity, 2)
)

c2.metric(
    "Median Activity Hours",
    round(median_activity, 2)
)
