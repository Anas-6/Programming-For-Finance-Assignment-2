import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# Function to fetch crypto prices with caching
@st.cache_data(ttl=60)  # Cache data for 60 seconds
def get_crypto_prices(cryptos):
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={",".join(cryptos)}&vs_currencies=usd'
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error if the request fails
        data = response.json()
        
        prices = {}
        for crypto in cryptos:
            if crypto in data and 'usd' in data[crypto]:
                prices[crypto] = data[crypto]['usd']
            else:
                prices[crypto] = None  # If no price found, return None

        return prices
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching prices: {e}")
        return {crypto: None for crypto in cryptos}  # Ensure consistent output format

# Function to calculate portfolio value
def calculate_portfolio_value(holdings, prices):
    total_value = 0
    for crypto, amount in holdings.items():
        price = prices.get(crypto)
        if isinstance(price, (int, float)):  # Check if price is valid
            total_value += amount * price
    return total_value

# Streamlit UI
st.set_page_config(page_title="Cryptocurrency Portfolio Tracker", page_icon="🪙", layout="wide")
st.title("🪙 Cryptocurrency Portfolio Tracker")
st.write("### Track your cryptocurrency portfolio performance and see your portfolio value.")

# Sidebar for Portfolio Details
st.sidebar.header("Portfolio Details")
cryptos = ['bitcoin', 'ethereum', 'cardano', 'dogecoin', 'litecoin']
holdings = {}

for crypto in cryptos:
    holdings[crypto] = st.sidebar.number_input(f"Amount of {crypto.capitalize()} (in coins)", min_value=0, value=0)

# Fetch Prices
st.write("⏳ Fetching latest prices...")
prices = get_crypto_prices(cryptos)

# Debugging: Show API response in Streamlit (remove later if not needed)
st.write("### API Response:")
st.json(prices)

# Display Prices in a Table
st.write("### Real-time Cryptocurrency Prices (USD)")
crypto_df = pd.DataFrame(prices.items(), columns=["Cryptocurrency", "Price (USD)"])
crypto_df['Price (USD)'] = crypto_df['Price (USD)'].apply(lambda x: "Data unavailable" if x is None else f"${x:.2f}")
st.write(crypto_df)

# Calculate Portfolio Value
portfolio_value = calculate_portfolio_value(holdings, prices)
st.write(f"### Total Portfolio Value: ${portfolio_value:.2f}")

# Portfolio Distribution Chart
portfolio_data = {
    "Cryptocurrency": [],
    "Amount": [],
    "Value (USD)": []
}

for crypto in cryptos:
    if holdings[crypto] > 0 and isinstance(prices.get(crypto), (int, float)):
        portfolio_data["Cryptocurrency"].append(crypto.capitalize())
        portfolio_data["Amount"].append(holdings[crypto])
        portfolio_data["Value (USD)"].append(holdings[crypto] * prices[crypto])

if portfolio_data["Cryptocurrency"]:
    # Custom colors (Cardano = Green, others default)
    colors = {crypto.capitalize(): "green" if crypto == "cardano" else None for crypto in cryptos}
    
    fig = px.pie(portfolio_data, values="Value (USD)", names="Cryptocurrency", title="Portfolio Distribution",
                 color="Cryptocurrency", color_discrete_map=colors)
    st.plotly_chart(fig)

# Bar Chart for Portfolio Value
if portfolio_data["Cryptocurrency"]:
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(portfolio_data["Cryptocurrency"], portfolio_data["Value (USD)"], color=['blue', 'red', 'green', 'purple', 'orange'])
    ax.set_title("Portfolio Value by Cryptocurrency")
    ax.set_xlabel("Cryptocurrency")
    ax.set_ylabel("Value in USD")
    st.pyplot(fig)

st.markdown("---")
st.write("🔹 Built with ❤️ using Streamlit | AF3005 - Programming for Finance | Instructor: Dr. Usama Arshad")
