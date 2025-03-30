import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Fetch real-time data from CoinGecko API
def get_crypto_prices(cryptos):
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={",".join(cryptos)}&vs_currencies=usd'
    response = requests.get(url)
    data = response.json()
    
    # Error handling to check if the data for each cryptocurrency is available
    prices = {}
    for crypto in cryptos:
        if crypto in data:
            prices[crypto] = data[crypto].get('usd', None)
        else:
            prices[crypto] = None  # Set to None if not available

    return prices

# Calculate the portfolio value
def calculate_portfolio_value(holdings, prices):
    total_value = sum(holdings[crypto] * prices.get(crypto, 0) for crypto in holdings)
    return total_value

# Streamlit Layout
st.set_page_config(page_title="Cryptocurrency Portfolio Tracker", page_icon="🪙", layout="wide")

st.title("🪙 Cryptocurrency Portfolio Tracker")
st.write("### Track your cryptocurrency portfolio performance and see your portfolio value.")

# Sidebar Inputs
st.sidebar.header("Portfolio Details")

# User inputs the amount of each cryptocurrency they hold
cryptos = ['bitcoin', 'ethereum', 'cardano', 'dogecoin', 'litecoin']  # Add more cryptos as needed
holdings = {}
for crypto in cryptos:
    holdings[crypto] = st.sidebar.number_input(f"Amount of {crypto.capitalize()} (in coins)", min_value=0, value=0)

# Fetch real-time crypto prices
prices = get_crypto_prices(cryptos)

# Show real-time prices for each cryptocurrency
st.write("### Real-time Cryptocurrency Prices (USD)")
crypto_df = pd.DataFrame(prices.items(), columns=["Cryptocurrency", "Price (USD)"])

# Handle cases where a cryptocurrency price might be unavailable (e.g., show a message or NaN)
crypto_df['Price (USD)'] = crypto_df['Price (USD)'].apply(lambda x: f"Data unavailable" if x is None else f"${x:.2f}")
st.write(crypto_df)

# Calculate total portfolio value
portfolio_value = calculate_portfolio_value(holdings, prices)

st.write(f"### Total Portfolio Value: ${portfolio_value:.2f}")

# Visualize Portfolio Distribution
portfolio_data = {"Cryptocurrency": [], "Amount": [], "Value (USD)": []}
for crypto in cryptos:
    if holdings[crypto] > 0 and prices.get(crypto, None) is not None:
        portfolio_data["Cryptocurrency"].append(crypto.capitalize())
        portfolio_data["Amount"].append(holdings[crypto])
        portfolio_data["Value (USD)"].append(holdings[crypto] * prices[crypto])

# Display pie chart for portfolio distribution
portfolio_df = pd.DataFrame(portfolio_data)
if len(portfolio_df) > 0:
    fig = px.pie(portfolio_df, values="Value (USD)", names="Cryptocurrency", title="Portfolio Distribution")
    st.plotly_chart(fig)

# Display bar chart for portfolio performance (Amount vs Value)
if len(portfolio_df) > 0:
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(portfolio_df["Cryptocurrency"], portfolio_df["Value (USD)"], color='royalblue')
    ax.set_title("Portfolio Value by Cryptocurrency")
    ax.set_xlabel("Cryptocurrency")
    ax.set_ylabel("Value in USD")
    st.pyplot(fig)

# Optional: Simple forecasting (based on price trends, if you want to add this feature)
st.markdown("---")
st.write("🔹 Built with ❤️ using Streamlit | AF3005 - Programming for Finance | Instructor: Dr. Usama Arshad")
