import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px


def get_crypto_prices(cryptos):
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={",".join(cryptos)}&vs_currencies=usd'
    response = requests.get(url)
    data = response.json()
    
   
    prices = {crypto: data[crypto]['usd'] for crypto in cryptos}
    return prices



def calculate_portfolio_value(holdings, prices):
    total_value = sum(holdings[crypto] * prices[crypto] for crypto in holdings)
    return total_value


st.set_page_config(page_title="Cryptocurrency Portfolio Tracker", page_icon="🪙", layout="wide")

st.title("🪙 Cryptocurrency Portfolio Tracker")
st.write("### Track your cryptocurrency portfolio performance and see your portfolio value.")

st.sidebar.header("Portfolio Details")



cryptos = ['bitcoin', 'ethereum', 'cardano', 'dogecoin', 'litecoin']  
holdings = {}
for crypto in cryptos:
    holdings[crypto] = st.sidebar.number_input(f"Amount of {crypto.capitalize()} (in coins)", min_value=0, value=0)


prices = get_crypto_prices(cryptos)



st.write("### Real-time Cryptocurrency Prices (USD)")
crypto_df = pd.DataFrame(prices.items(), columns=["Cryptocurrency", "Price (USD)"])
st.write(crypto_df)



portfolio_value = calculate_portfolio_value(holdings, prices)

st.write(f"### Total Portfolio Value: ${portfolio_value:.2f}")



portfolio_data = {"Cryptocurrency": [], "Amount": [], "Value (USD)": []}
for crypto in cryptos:
    if holdings[crypto] > 0:
        portfolio_data["Cryptocurrency"].append(crypto.capitalize())
        portfolio_data["Amount"].append(holdings[crypto])
        portfolio_data["Value (USD)"].append(holdings[crypto] * prices[crypto])



portfolio_df = pd.DataFrame(portfolio_data)
if len(portfolio_df) > 0:
    fig = px.pie(portfolio_df, values="Value (USD)", names="Cryptocurrency", title="Portfolio Distribution")
    st.plotly_chart(fig)



if len(portfolio_df) > 0:
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(portfolio_df["Cryptocurrency"], portfolio_df["Value (USD)"], color='royalblue')
    ax.set_title("Portfolio Value by Cryptocurrency")
    ax.set_xlabel("Cryptocurrency")
    ax.set_ylabel("Value in USD")
    st.pyplot(fig)



st.markdown("---")
st.write("🔹 Built with ❤️ using Streamlit | AF3005 - Programming for Finance | Instructor: Dr. Usama Arshad")
