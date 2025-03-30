import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# Function to fetch crypto prices in selected currency
@st.cache_data(ttl=60)  # Cache for 60 seconds to avoid API rate limits
def get_crypto_prices(cryptos, currency):
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={",".join(cryptos)}&vs_currencies={currency.lower()}'
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise error if request fails
        data = response.json()
        
        prices = {crypto: data.get(crypto, {}).get(currency.lower(), None) for crypto in cryptos}
        return prices
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching prices: {e}")
        return {crypto: None for crypto in cryptos}

# Function to calculate portfolio value
def calculate_portfolio_value(holdings, prices):
    return sum(holdings[crypto] * prices.get(crypto, 0) for crypto in holdings)

# Streamlit UI
st.set_page_config(page_title="Cryptocurrency Portfolio Tracker", page_icon="🪙", layout="wide")
st.title("🪙 Cryptocurrency Portfolio Tracker")
st.write("### Track your cryptocurrency portfolio performance in your preferred currency.")

# Sidebar for Portfolio Details
st.sidebar.header("Portfolio Details")

# Currency selection
currencies = ["USD", "EUR", "GBP", "PKR", "AUD", "CAD", "INR", "JPY"]  # Add more as needed
selected_currency = st.sidebar.selectbox("Select Currency", currencies, index=0)

# Supported cryptocurrencies
cryptos = ['bitcoin', 'ethereum', 'cardano', 'dogecoin', 'litecoin']
holdings = {crypto: st.sidebar.number_input(f"Amount of {crypto.capitalize()} (in coins)", min_value=0, value=0) for crypto in cryptos}

# Fetch Prices
st.write("⏳ Fetching latest prices...")
prices = get_crypto_prices(cryptos, selected_currency)

# Display Prices in a Table
st.write(f"### Real-time Cryptocurrency Prices ({selected_currency})")
crypto_df = pd.DataFrame(prices.items(), columns=["Cryptocurrency", f"Price ({selected_currency})"])
crypto_df[f"Price ({selected_currency})"] = crypto_df[f"Price ({selected_currency})"].apply(lambda x: "Data unavailable" if x is None else f"{x:.2f} {selected_currency}")
st.write(crypto_df)

# Calculate Portfolio Value
portfolio_value = calculate_portfolio_value(holdings, prices)
st.write(f"### Total Portfolio Value: {portfolio_value:.2f} {selected_currency}")

# Portfolio Distribution Chart
portfolio_data = {
    "Cryptocurrency": [],
    "Amount": [],
    f"Value ({selected_currency})": []
}

for crypto in cryptos:
    price = prices.get(crypto)
    if holdings[crypto] > 0 and isinstance(price, (int, float)):
        portfolio_data["Cryptocurrency"].append(crypto.capitalize())
        portfolio_data["Amount"].append(holdings[crypto])
        portfolio_data[f"Value ({selected_currency})"].append(holdings[crypto] * price)

# Ensure charts render only if there is valid data
if portfolio_data["Cryptocurrency"]:
    # 🎨 Updated high-contrast colors for pie chart
    pie_colors = {
        "Bitcoin": "#ffcc00",  # Gold
        "Ethereum": "#3c3c3d",  # Dark Gray
        "Cardano": "#009933",  # Green (as requested)
        "Dogecoin": "#ba9f33",  # Yellowish Brown
        "Litecoin": "#bfbfbf",  # Silver
    }

    fig = px.pie(portfolio_data, values=f"Value ({selected_currency})", names="Cryptocurrency", title="Portfolio Distribution",
                 color="Cryptocurrency", color_discrete_map=pie_colors)
    st.plotly_chart(fig)

# 🎨 Updated Bar Chart with working colors for all cryptos
if portfolio_data["Cryptocurrency"]:
    fig, ax = plt.subplots(figsize=(10, 6))
    
    bar_colors = ['#ff9900', '#0000ff', '#009933', '#ff6600', '#6600cc']  # Contrast colors for bars
    ax.bar(portfolio_data["Cryptocurrency"], portfolio_data[f"Value ({selected_currency})"], color=bar_colors[:len(portfolio_data["Cryptocurrency"])])
    
    ax.set_title("Portfolio Value by Cryptocurrency")
    ax.set_xlabel("Cryptocurrency")
    ax.set_ylabel(f"Value in {selected_currency}")
    
    st.pyplot(fig)

st.markdown("---")
st.write("🔹 Built with ❤️ using Streamlit | AF3005 - Programming for Finance | Instructor: Dr. Usama Arshad")
