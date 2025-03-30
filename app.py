import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt


@st.cache_data(ttl=60)  
def get_crypto_prices(cryptos):
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={",".join(cryptos)}&vs_currencies=usd'
    
    try:
        response = requests.get(url)
        response.raise_for_status() 
        data = response.json()
        
        prices = {crypto: data.get(crypto, {}).get('usd', None) for crypto in cryptos}
        return prices
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching prices: {e}")
        return {crypto: None for crypto in cryptos}  


def calculate_portfolio_value(holdings, prices):
    return sum(holdings[crypto] * prices.get(crypto, 0) for crypto in holdings)


st.set_page_config(page_title="Cryptocurrency Portfolio Tracker", page_icon="🪙", layout="wide")
st.title("₿ Cryptocurrency Portfolio Tracker")
st.write("### Track your cryptocurrency portfolio performance and see your portfolio value.")



st.sidebar.header("Portfolio Details")
cryptos = ['bitcoin', 'ethereum', 'cardano', 'dogecoin', 'litecoin']
holdings = {crypto: st.sidebar.number_input(f"Amount of {crypto.capitalize()} (in coins)", min_value=0, value=0) for crypto in cryptos}


st.write("⏳ Fetching latest prices...")
prices = get_crypto_prices(cryptos)



st.write("### Real-time Cryptocurrency Prices (USD)")
crypto_df = pd.DataFrame(prices.items(), columns=["Cryptocurrency", "Price (USD)"])
crypto_df['Price (USD)'] = crypto_df['Price (USD)'].apply(lambda x: "Data unavailable" if x is None else f"${x:.2f}")
st.write(crypto_df)



portfolio_value = calculate_portfolio_value(holdings, prices)
st.write(f"### Total Portfolio Value: ${portfolio_value:.2f}")



portfolio_data = {
    "Cryptocurrency": [],
    "Amount": [],
    "Value (USD)": []
}

for crypto in cryptos:
    price = prices.get(crypto)
    if holdings[crypto] > 0 and isinstance(price, (int, float)):
        portfolio_data["Cryptocurrency"].append(crypto.capitalize())
        portfolio_data["Amount"].append(holdings[crypto])
        portfolio_data["Value (USD)"].append(holdings[crypto] * price)



if portfolio_data["Cryptocurrency"]:
   
    pie_colors = {
        "Bitcoin": "#ffcc00",  # Gold
        "Ethereum": "#3c3c3d",  # Dark Gray
        "Cardano": "#009933",  # Green (as requested)
        "Dogecoin": "#ba9f33",  # Yellowish Brown
        "Litecoin": "#bfbfbf",  # Silver
    }

    fig = px.pie(portfolio_data, values="Value (USD)", names="Cryptocurrency", title="Portfolio Distribution",
                 color="Cryptocurrency", color_discrete_map=pie_colors)
    st.plotly_chart(fig)


if portfolio_data["Cryptocurrency"]:
    fig, ax = plt.subplots(figsize=(10, 6))
    
    bar_colors = ['#ff9900', '#0000ff', '#009933', '#ff6600', '#6600cc']  
    ax.bar(portfolio_data["Cryptocurrency"], portfolio_data["Value (USD)"], color=bar_colors[:len(portfolio_data["Cryptocurrency"])])
    
    ax.set_title("Portfolio Value by Cryptocurrency")
    ax.set_xlabel("Cryptocurrency")
    ax.set_ylabel("Value in USD")
    
    st.pyplot(fig)

st.markdown("---")
st.write("🔹 Built with ❤️ using Streamlit | AF3005 - Programming for Finance | Instructor: Dr. Usama Arshad")