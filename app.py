import streamlit as st
import matplotlib.pyplot as plt
from forex_python.converter import CurrencyRates
import pandas as pd
import numpy as np

currency_rates = CurrencyRates()

st.set_page_config(page_title="Forex Exchange Rate Tracker", page_icon="💹", layout="wide")

st.title("💹 Forex Exchange Rate Tracker")
st.write("### Track the latest exchange rates between any two currencies.")
st.write("This app allows you to check the exchange rates and visualize historical trends for any currency pair.")
st.write("Additionally, it can forecast future exchange rates using a simple statistical method.")

st.sidebar.header("Select Currencies")

base_currency = st.sidebar.selectbox("Choose base currency", ['USD', 'EUR', 'GBP', 'INR', 'AUD', 'CAD', 'JPY', 'CHF', 'CNY'])
target_currency = st.sidebar.selectbox("Choose target currency", ['USD', 'EUR', 'GBP', 'INR', 'AUD', 'CAD', 'JPY', 'CHF', 'CNY'])

# Error handling for currency rates fetching
try:
    latest_rate = currency_rates.get_rate(base_currency, target_currency)
    st.write(f"### Latest Exchange Rate: 1 {base_currency} = {latest_rate:.2f} {target_currency}")
except Exception as e:
    st.error(f"Error fetching exchange rate: {e}")
    latest_rate = None

start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2021-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("2023-01-01"))

forecast_days = st.sidebar.slider("Number of Days to Forecast", min_value=1, max_value=30, value=7)

# Fetch historical data only if latest_rate is successfully retrieved
if latest_rate:
    dates = pd.date_range(start_date, end_date)
    rates = []
    
    # Handling errors when fetching historical data
    for date in dates:
        try:
            rate = currency_rates.get_rate(base_currency, target_currency, date)
            rates.append(rate)
        except Exception as e:
            st.warning(f"Error fetching rate for {date}: {e}")
            rates.append(np.nan)  # Placeholder for missing data

    historical_data = pd.DataFrame({
        "Date": dates,
        "Exchange Rate": rates
    })
    
    historical_data["SMA"] = historical_data["Exchange Rate"].rolling(window=forecast_days).mean()

    forecast_dates = pd.date_range(dates[-1] + pd.Timedelta(days=1), periods=forecast_days)

    forecast_values = [historical_data["SMA"].iloc[-1]] * forecast_days  # Use the last SMA value to predict future rates

    st.write(f"### {forecast_days}-Day Forecast for {base_currency} to {target_currency}")
    forecast_data = pd.DataFrame({
        "Date": forecast_dates,
        "Forecasted Rate": forecast_values
    })
    st.write(forecast_data)

    st.write("### Historical Exchange Rate with Forecast")

    # Plotting the data
    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(historical_data["Date"], historical_data["Exchange Rate"], label=f"{base_currency}/{target_currency} Rate", color='blue')
    ax.plot(historical_data["Date"], historical_data["SMA"], label=f"{forecast_days}-Day SMA", color='green', linestyle='--')
    ax.plot(forecast_data["Date"], forecast_data["Forecasted Rate"], label="Forecasted Rate", color='red', linestyle=':')

    ax.set_xlabel("Date")
    ax.set_ylabel("Exchange Rate")
    ax.set_title(f"Exchange Rate Trend: {base_currency} to {target_currency} with {forecast_days}-Day Forecast")
    ax.legend()
    st.pyplot(fig)

else:
    st.error("Unable to retrieve exchange rates. Please check your currency pair selection.")

st.markdown("---")
st.write("🔹 Built with ❤️ using Streamlit | AF3005 - Programming for Finance | Instructor: Dr. Usama Arshad")
