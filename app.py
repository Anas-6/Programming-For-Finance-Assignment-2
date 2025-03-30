import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt


@st.cache_data(ttl=3600)  
def get_all_cryptos():
    url = "https://api.coingecko.com/api/v3/coins/list"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return [coin["id"] for coin in response.json()]
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching cryptocurrencies: {e}")
        return []


@st.cache_data(ttl=60)  
def get_crypto_prices(selected_cryptos, currency):
    if not selected_cryptos:
        return {}

    url = f'https://api.coingecko.com/api/v3/simple/price?ids={",".join(selected_cryptos)}&vs_currencies={currency.lower()}'
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        return {crypto: data.get(crypto, {}).get(currency.lower(), None) for crypto in selected_cryptos}
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching prices: {e}")
        return {crypto: None for crypto in selected_cryptos}


def calculate_portfolio_value(holdings, prices):
    return sum(holdings[crypto] * prices.get(crypto, 0) for crypto in holdings)


st.set_page_config(page_title="Cryptocurrency Portfolio Tracker", page_icon="🪙", layout="wide")
st.title("🪙 Cryptocurrency Portfolio Tracker")
st.write("### Track your cryptocurrency portfolio in your preferred currency with live market data.")


st.sidebar.header("Portfolio Details")


currencies = ["USD", "EUR", "GBP", "PKR", "AUD", "CAD", "INR", "JPY"]  
selected_currency = st.sidebar.selectbox("Select Currency", currencies, index=0)


st.sidebar.write("🔍 **Select Cryptocurrencies to Track**")
all_cryptos = get_all_cryptos()
selected_cryptos = st.sidebar.multiselect("Search and select cryptos", all_cryptos, default=["bitcoin", "ethereum", "cardano", "dogecoin", "litecoin"])


holdings = {crypto: st.sidebar.number_input(f"Amount of {crypto.capitalize()} (in coins)", min_value=0.0, value=0.0, format="%.6f") for crypto in selected_cryptos}


st.write("⏳ Fetching latest prices...")
prices = get_crypto_prices(selected_cryptos, selected_currency)


st.write(f"### Real-time Cryptocurrency Prices ({selected_currency})")
crypto_df = pd.DataFrame(prices.items(), columns=["Cryptocurrency", f"Price ({selected_currency})"])
crypto_df[f"Price ({selected_currency})"] = crypto_df[f"Price ({selected_currency})"].apply(lambda x: "Data unavailable" if x is None else f"{x:.6f} {selected_currency}")
st.write(crypto_df)


portfolio_value = calculate_portfolio_value(holdings, prices)
st.write(f"### Total Portfolio Value: {portfolio_value:.2f} {selected_currency}")


portfolio_data = {
    "Cryptocurrency": [],
    "Amount": [],
    f"Value ({selected_currency})": []
}

for crypto in selected_cryptos:
    price = prices.get(crypto)
    if holdings[crypto] > 0 and isinstance(price, (int, float)):
        portfolio_data["Cryptocurrency"].append(crypto.capitalize())
        portfolio_data["Amount"].append(holdings[crypto])
        portfolio_data[f"Value ({selected_currency})"].append(holdings[crypto] * price)


if portfolio_data["Cryptocurrency"]:
    
    fig = px.pie(portfolio_data, values=f"Value ({selected_currency})", names="Cryptocurrency", title="Portfolio Distribution")
    st.plotly_chart(fig)


if portfolio_data["Cryptocurrency"]:
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.bar(portfolio_data["Cryptocurrency"], portfolio_data[f"Value ({selected_currency})"], color=['#ff9900', '#0000ff', '#009933', '#ff6600', '#6600cc'][:len(portfolio_data["Cryptocurrency"])])
    
    ax.set_title("Portfolio Value by Cryptocurrency")
    ax.set_xlabel("Cryptocurrency")
    ax.set_ylabel(f"Value in {selected_currency}")
    
    st.pyplot(fig)

st.markdown("---")
st.write("🔹 Built with ❤️ using Streamlit | AF3005 - Programming for Finance | Instructor: Dr. Usama Arshad")