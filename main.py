import streamlit as st
import pandas as pd
import plotly.express as px
from forex_python.converter import CurrencyRates

# App Config
st.set_page_config(page_title="Forex Tracker", layout="wide")
st.title("💱 Forex Exchange Rate Tracker")

# Sidebar Controls
with st.sidebar:
    st.header("Settings")
    base_currency = st.selectbox("Base Currency", ["USD", "EUR", "GBP", "JPY", "PKR"])
    target_currencies = st.multiselect(
        "Target Currencies", 
        ["USD", "EUR", "GBP", "JPY", "AUD", "CAD", "CNY", "PKR"],
        default=["EUR", "GBP"]
    )
    days = st.slider("Historical Data (Days)", 1, 365, 30)

# Fetch Data
@st.cache_data
def get_rates(base, targets, days_back):
    c = CurrencyRates()
    end_date = pd.Timestamp.now()
    start_date = end_date - pd.Timedelta(days=days_back)
    
    dates = pd.date_range(start_date, end_date)
    df = pd.DataFrame(index=dates, columns=targets)
    
    for date in dates:
        for currency in targets:
            try:
                df.loc[date, currency] = c.get_rate(base, currency, date)
            except:
                df.loc[date, currency] = None
                
    return df.dropna()

if target_currencies:
    with st.spinner("Fetching exchange rates..."):
        df = get_rates(base_currency, target_currencies, days)
    
    # Current Rates
    st.header(f"Current Rates (1 {base_currency})")
    cols = st.columns(len(target_currencies))
    for col, currency in zip(cols, target_currencies):
        col.metric(currency, f"{df.iloc[-1][currency]:.4f}")

    # Historical Chart
    st.header("Historical Trends")
    fig = px.line(df, title=f"{base_currency} Exchange Rate History")
    st.plotly_chart(fig, use_container_width=True)
    
    # Raw Data
    st.header("Raw Data")
    st.dataframe(df.style.highlight_max(axis=0))
else:
    st.warning("Select at least one target currency")