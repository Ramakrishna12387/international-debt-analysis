
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="International Debt Analysis",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 International Debt Analysis Dashboard")
st.caption("External debt per capita (US$) | Historical data")

@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_international_debt.csv")
    df["year"] = df["year"].astype(int)
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")

countries = sorted(df["country_name"].unique())
selected_country = st.sidebar.selectbox(
    "Select Country",
    countries
)

min_year = int(df["year"].min())
max_year = int(df["year"].max())

selected_years = st.sidebar.slider(
    "Select Year Range",
    min_value=min_year,
    max_value=max_year,
    value=(max_year - 10, max_year)
)

filtered = df[
    (df["country_name"] == selected_country)
    & (df["year"] >= selected_years[0])
    & (df["year"] <= selected_years[1])
].sort_values("year")

# KPI cards
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Countries in Dataset", df["country_name"].nunique())

with col2:
    st.metric("Available Records", len(filtered))

with col3:
    if not filtered.empty:
        st.metric(
            "Latest Available Value",
            f"${filtered.iloc[-1]['debt']:,.2f}"
        )
    else:
        st.metric("Latest Available Value", "No data")

st.divider()

st.subheader(f"Debt Per Capita Trend — {selected_country}")

if not filtered.empty:
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(filtered["year"], filtered["debt"], marker="o")
    ax.set_xlabel("Year")
    ax.set_ylabel("External Debt Per Capita (US$)")
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)
    plt.close(fig)
else:
    st.info("No data available for this selection.")

st.subheader("Top 10 Countries by Historical Average")

top10 = (
    df.groupby("country_name")["debt"]
    .mean()
    .nlargest(10)
    .sort_values()
)

fig2, ax2 = plt.subplots(figsize=(10, 5))
top10.plot(kind="barh", ax=ax2)
ax2.set_xlabel("Average External Debt Per Capita (US$)")
st.pyplot(fig2)
plt.close(fig2)

st.subheader("Data Preview")
st.dataframe(filtered, use_container_width=True)

st.download_button(
    "Download Filtered Data as CSV",
    data=filtered.to_csv(index=False).encode("utf-8"),
    file_name="filtered_debt_data.csv",
    mime="text/csv"
)
