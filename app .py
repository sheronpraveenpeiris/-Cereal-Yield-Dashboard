# Import necessary Librkes
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Cereal Yield Dashboard", layout="wide")

# Load dataset
df = pd.read_excel("cereal_yield.xlsx")

# Rename columns
df.columns = ["Country", "Year", "Yield"]

# Clean data
df = df.dropna()
df["Year"] = df["Year"].astype(int)
df["Yield"] = df["Yield"].astype(float)

# Filter base years
df = df[(df["Year"] >= 2010) & (df["Year"] <= 2022)]

#  sidebar added
st.sidebar.header(" Filters")

country = st.sidebar.selectbox(
    "Select Country",
    sorted(df["Country"].unique())
)

year_range = st.sidebar.slider(
    "Select Year Range",
    int(df["Year"].min()),
    int(df["Year"].max()),
    (2010, 2022)
)

# Filtered data
filtered = df[
    (df["Country"] == country) &
    (df["Year"] >= year_range[0]) &
    (df["Year"] <= year_range[1])
]

#Title
st.title("  Global Cereal Yield Dashboard")


col1, col2, col3 = st.columns(3)

col1.metric("Country", country)
col2.metric("Avg Yield", f"{filtered['Yield'].mean():,.0f}")
col3.metric("Latest Year", int(filtered["Year"].max()))


chart1, chart2 = st.columns(2)

with chart1:
    st.subheader(f"{country} Yield Trend")
    fig1 = px.line(
        filtered,
        x="Year",
        y="Yield",
        markers=True,
        title=f"Cereal Yield Trend in {country}"
    )
    fig1.update_layout(xaxis_title="Year", yaxis_title="Yield")
    st.plotly_chart(fig1, use_container_width=True)

with chart2:
    st.subheader("Global Average Trend")
    avg = df.groupby("Year")["Yield"].mean().reset_index()
    fig2 = px.line(
        avg,
        x="Year",
        y="Yield",
        markers=True,
        title="Global Average Cereal Yield"
    )
    fig2.update_layout(xaxis_title="Year", yaxis_title="Yield")
    st.plotly_chart(fig2, use_container_width=True)

# charts added
st.subheader("Top 10 Countries (Latest Year)")

latest_year = df["Year"].max()
top10 = df[df["Year"] == latest_year].sort_values(by="Yield", ascending=False).head(10)

fig3 = px.bar(
    top10,
    x="Yield",
    y="Country",
    orientation="h",
    text="Yield",
    title=f"Top 10 Countries in {latest_year}"
)

fig3.update_layout(
    height=500,
    xaxis_title="Yield",
    yaxis_title="Country",
    yaxis={"categoryorder": "total ascending"}
)

fig3.update_traces(texttemplate="%{text:,.0f}", textposition="outside")

st.plotly_chart(fig3, use_container_width=True)


st.subheader("Key Insights")

st.write("""
- Cereal yield shows a clear upward trend over recent years.
- Some countries significantly outperform others in agricultural productivity.
- The global average indicates steady improvement in food production.
- The top-performing countries demonstrate advanced agricultural efficiency.
""")

