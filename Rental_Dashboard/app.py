import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt


st.set_page_config(page_title="Rental Prices in Germany", layout="wide")

st.title("🏠 Rental Prices in Germany")
st.markdown("Explore apartment rental prices across German cities 📊")
st.write("#")


@st.cache_data
def load_data():
    df = pd.read_csv("Rental_Dashboard/data/immo_data_cleaned.csv")
    df["date"] = pd.to_datetime(df["date"], errors='coerce')
    return df.dropna(subset=["totalRent", "city"])

df = load_data()

st.sidebar.header("🔍 Filters")
cities = df["city"].unique()
selected_cities = st.sidebar.multiselect("Select Cities:", options=cities, default=cities[:5])

min_price, max_price = int(df["totalRent"].min()), int(df["totalRent"].max())
price_range = st.sidebar.slider("Rental Price Range (€):", min_price, max_price, (min_price, max_price))

filtered_df = df[
    (df["city"].isin(selected_cities)) &
    (df["totalRent"] >= price_range[0]) &
    (df["totalRent"] <= price_range[1])
]

st.subheader("📈 Overview Stats")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Average Rent (€)", f"{filtered_df['totalRent'].mean():.0f}")
with col2:
    st.metric("Total Listings", len(filtered_df))
with col3:
    st.metric("Cities Selected", len(selected_cities))

st.write("#")
st.subheader("💰 Rental Price Distribution")
fig1, ax1 = plt.subplots(figsize=(10, 4))
sns.histplot(filtered_df["totalRent"], bins=40, kde=True, ax=ax1)
st.pyplot(fig1)

st.write("#")
st.subheader("🏙️ Average Rental Price by City")

avg_rent_by_city = (
    filtered_df.groupby("city")["totalRent"]
    .mean()
    .reset_index()
    .sort_values(by="totalRent", ascending=False)
)

bar_chart = alt.Chart(avg_rent_by_city).mark_bar().encode(
    x=alt.X("city:N", title="City", sort="-y", axis=alt.Axis(labelAngle=45)),
    y=alt.Y("totalRent:Q", title="Average Rent (€)"),
    tooltip=[
        alt.Tooltip("city:N", title="City"),
        alt.Tooltip("totalRent:Q", title="Average Rent (€)", format=".2f")
    ]
).properties(
    width='container',
    height=400,
    title="Average Rent per City (Hover to see exact value)"
).configure_axis(
    labelFontSize=12,
    titleFontSize=14,
    labelPadding=10
).configure_view(
    strokeWidth=0  # Remove border around the plot
).configure_mark(
    color='steelblue'  # Simple bar color
)

st.altair_chart(bar_chart, use_container_width=True)


st.write("#")
with st.expander("🔎 Show Raw Data"):
    st.dataframe(filtered_df.reset_index(drop=True))

st.write("##")
st.write("Source for The Data --> https://www.kaggle.com/code/bennerlukas/german-rental-prices")
