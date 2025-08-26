
import streamlit as st
import pandas as pd
import plotly.express as px
from io import StringIO

st.set_page_config(page_title="Crime Rate Analysis", page_icon="📊", layout="wide")

st.title("📊 Crime Rate Analysis Dashboard")
st.markdown(
    "Analyze crime patterns over time, compare across states/cities, and explore crime types. "
    "Use the sidebar to filter and upload your own CSV (optional)."
)

@st.cache_data
def load_sample():
    return pd.read_csv("data/sample_crime_data.csv")

def validate_cols(df):
    required = {"year","month","state","city","crime_type","incidents","population"}
    missing = required - set(df.columns)
    return missing

# Sidebar: data source
st.sidebar.header("Data")
use_sample = st.sidebar.toggle("Use sample dataset", value=True)
uploaded = st.sidebar.file_uploader("Or upload CSV with columns: year, month, state, city, crime_type, incidents, population", type=["csv"])

if not use_sample and uploaded is not None:
    try:
        data = pd.read_csv(uploaded)
    except Exception:
        # try with utf-16 etc.
        uploaded.seek(0)
        data = pd.read_csv(uploaded, encoding_errors="ignore")
else:
    data = load_sample()

# Basic cleaning
data["year"] = pd.to_numeric(data["year"], errors="coerce").astype("Int64")
data["month"] = pd.to_numeric(data["month"], errors="coerce").astype("Int64")
data["incidents"] = pd.to_numeric(data["incidents"], errors="coerce")
data["population"] = pd.to_numeric(data["population"], errors="coerce")

# Validate
missing = validate_cols(data)
if missing:
    st.error(f"Your dataset is missing columns: {missing}")
    st.stop()

# Derived metric: crime rate per 100k
data["crime_rate_per_100k"] = (data["incidents"] / data["population"]) * 100000

# Sidebar filters
st.sidebar.header("Filters")
years = sorted([x for x in data["year"].dropna().unique()])
year_sel = st.sidebar.multiselect("Year", years, default=years[-3:] if len(years)>=3 else years)
states = sorted([x for x in data["state"].dropna().unique()])
state_sel = st.sidebar.multiselect("State", states, default=states[:5])
crime_types = sorted([x for x in data["crime_type"].dropna().unique()])
crime_sel = st.sidebar.multiselect("Crime Type", crime_types, default=crime_types[:4])

df = data.copy()
if year_sel:
    df = df[df["year"].isin(year_sel)]
if state_sel:
    df = df[df["state"].isin(state_sel)]
if crime_sel:
    df = df[df["crime_type"].isin(crime_sel)]

# Top KPIs
total_incidents = int(df["incidents"].sum())
avg_rate = df["crime_rate_per_100k"].mean()
unique_cities = df["city"].nunique()

c1, c2, c3 = st.columns(3)
c1.metric("Total Incidents (filtered)", f"{total_incidents:,}")
c2.metric("Avg Crime Rate / 100k", f"{avg_rate:,.2f}")
c3.metric("Cities Covered", f"{unique_cities:,}")

st.divider()

# Charts
tab1, tab2, tab3 = st.tabs(["📈 Trends", "🏙️ Geography (state/city)", "🧩 Crime Type Mix"])

with tab1:
    # Yearly trend
    trend = df.groupby(["year"], as_index=False)["incidents"].sum()
    if not trend.empty:
        fig = px.line(trend, x="year", y="incidents", markers=True, title="Incidents Over Years (Filtered)")
        st.plotly_chart(fig, use_container_width=True)
    # Monthly trend
    monthly = df.groupby(["year","month"], as_index=False)["incidents"].sum()
    if not monthly.empty:
        monthly["year_month"] = monthly["year"].astype(str) + "-" + monthly["month"].astype(str).str.zfill(2)
        fig2 = px.bar(monthly, x="year_month", y="incidents", title="Monthly Incidents", labels={"year_month":"Year-Month"})
        st.plotly_chart(fig2, use_container_width=True)

with tab2:
    by_state = df.groupby("state", as_index=False).agg({"incidents":"sum","population":"sum"})
    if not by_state.empty:
        by_state["rate_100k"] = (by_state["incidents"]/by_state["population"])*100000
        fig3 = px.bar(by_state.sort_values("rate_100k", ascending=False), x="state", y="rate_100k",
                      title="Crime Rate per 100k by State")
        st.plotly_chart(fig3, use_container_width=True)

    by_city = df.groupby(["state","city"], as_index=False).agg({"incidents":"sum","population":"sum"})
    if not by_city.empty:
        by_city["rate_100k"] = (by_city["incidents"]/by_city["population"])*100000
        fig4 = px.scatter(by_city, x="population", y="incidents", size="rate_100k",
                          hover_data=["state","city"], title="City-wise Incidents vs Population (bubble ~ rate/100k)")
        st.plotly_chart(fig4, use_container_width=True)

with tab3:
    mix = df.groupby("crime_type", as_index=False)["incidents"].sum().sort_values("incidents", ascending=False)
    if not mix.empty:
        fig5 = px.pie(mix, names="crime_type", values="incidents", title="Crime Type Composition (Incidents)")
        st.plotly_chart(fig5, use_container_width=True)

st.divider()
st.subheader("Raw Data (filtered)")
st.dataframe(df.sample(min(len(df), 100)).sort_values(["year","state","city","crime_type"]).reset_index(drop=True))
