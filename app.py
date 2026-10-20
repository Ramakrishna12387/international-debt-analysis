import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
from urllib.parse import quote_plus

st.set_page_config(page_title="International Debt Analytics", layout="wide", page_icon="🌐")

# ==========================================
# 1. DATABASE CONFIGURATION
# ==========================================
DB_USER = "root"
# UNGALODA MYSQL PASSWORD-AH INGA TYPE PANNUMGA:
RAW_PASSWORD = "root"

DB_PASS = quote_plus(RAW_PASSWORD)
DB_HOST = "localhost"
DB_PORT = "3306"
DB_NAME = "international_debt_db"

@st.cache_resource
def get_connection():
    return create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

try:
    engine = get_connection()
except Exception as e:
    st.error(f"Database Connection Error: {e}")
    st.stop()

# ==========================================
# 2. HEADER & KPI METRICS
# ==========================================
st.title("🌐 International Debt Analysis Dashboard")
st.markdown("Comprehensive insights and visualization of country-wise and indicator-wise global debt.")

metrics_query = """
SELECT 
    COALESCE((SELECT SUM(debt) FROM debt_data), 0) AS total_debt,
    COALESCE((SELECT COUNT(DISTINCT country_code) FROM countries), 0) AS total_countries,
    COALESCE((SELECT COUNT(DISTINCT indicator_code) FROM indicators), 0) AS total_indicators;
"""

try:
    metrics_df = pd.read_sql(metrics_query, engine)
    total_debt_val = float(metrics_df['total_debt'][0]) if not pd.isna(metrics_df['total_debt'][0]) else 0.0
    total_countries_val = int(metrics_df['total_countries'][0]) if not pd.isna(metrics_df['total_countries'][0]) else 0
    total_indicators_val = int(metrics_df['total_indicators'][0]) if not pd.isna(metrics_df['total_indicators'][0]) else 0
except Exception as e:
    total_debt_val, total_countries_val, total_indicators_val = 0.0, 0, 0

col1, col2, col3 = st.columns(3)
col1.metric("Global Total Debt", f"${total_debt_val:,.0f}")
col2.metric("Total Countries", total_countries_val)
col3.metric("Total Indicators", total_indicators_val)

st.divider()

if total_debt_val == 0:
    st.warning("⚠️ Table-la innum data illa! Mudhalla terminal-la `python data_pipeline.py` run panni data-va load pannunga.")
    st.stop()

# ==========================================
# 3. INTERACTIVE VISUALIZATIONS TABS
# ==========================================
tab1, tab2, tab3 = st.tabs(["Top Indebted Countries", "Indicator Insights", "Country Deep-Dive"])

with tab1:
    st.subheader("Top 10 Most Indebted Countries")
    top_country_query = """
    SELECT c.country_name, SUM(d.debt) AS total_debt
    FROM countries c
    JOIN debt_data d ON c.country_code = d.country_code
    GROUP BY c.country_name
    ORDER BY total_debt DESC
    LIMIT 10;
    """
    top_df = pd.read_sql(top_country_query, engine)
    if not top_df.empty:
        fig1 = px.bar(
            top_df, 
            x='country_name', 
            y='total_debt', 
            text_auto='.2s',
            title="Top 10 Countries with Highest Debt", 
            color='total_debt',
            color_continuous_scale="Reds",
            labels={'country_name': 'Country', 'total_debt': 'Total Debt (USD)'}
        )
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.info("No country records found.")

with tab2:
    st.subheader("Top 5 Debt Indicators")
    indicator_query = """
    SELECT i.indicator_name, SUM(d.debt) AS total_debt
    FROM indicators i
    JOIN debt_data d ON i.indicator_code = d.indicator_code
    GROUP BY i.indicator_name
    ORDER BY total_debt DESC
    LIMIT 5;
    """
    ind_df = pd.read_sql(indicator_query, engine)
    if not ind_df.empty:
        fig2 = px.pie(
            ind_df, 
            values='total_debt', 
            names='indicator_name',
            title="Top 5 Indicator Contribution to Global Debt",
            hole=0.4
        )
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("No indicator records found.")

with tab3:
    st.subheader("Country-Specific Indicator Breakdown")
    countries_query = "SELECT DISTINCT country_name FROM countries ORDER BY country_name;"
    countries_list = pd.read_sql(countries_query, engine)['country_name'].tolist()

    if countries_list:
        selected_country = st.selectbox("Select a country:", countries_list)

        country_breakdown_query = f"""
        SELECT i.indicator_name, d.debt
        FROM debt_data d
        JOIN countries c ON d.country_code = c.country_code
        JOIN indicators i ON d.indicator_code = i.indicator_code
        WHERE c.country_name = %(country)s
        ORDER BY d.debt DESC;
        """
        country_df = pd.read_sql(country_breakdown_query, engine, params={"country": selected_country})

        if not country_df.empty:
            fig3 = px.bar(
                country_df, 
                x='debt', 
                y='indicator_name', 
                orientation='h',
                title=f"Debt Breakdown for {selected_country}", 
                color='debt',
                labels={'debt': 'Debt Amount (USD)', 'indicator_name': 'Indicator'}
            )
            st.plotly_chart(fig3, use_container_width=True)
            st.dataframe(country_df, use_container_width=True)
        else:
            st.info(f"No debt records found for {selected_country}.")
    else:
        st.info("Country list is currently empty.")