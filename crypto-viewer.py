import streamlit as st
import pandas as pd
from PIL import Image
import base64
import matplotlib.pyplot as plt
from scrape_data import *

# Set Page width
st.set_page_config(layout="wide")


# Logo
# image = Image.open('logo.jpg')
# st.image(image, width = 500)

# Title
st.title('Crypto Price App')
st.markdown("""
This app retrieves cryptocurrency prices for the top 100 cryptocurrency from the **CoinMarketCap**!

-by Mayur Machhi
""")

# Page layout
sid = st.sidebar # Sidebar
col1, col2 = st.beta_columns((2,1)) # Main page


# currency_price_unit = col1.selectbox('Select currency for price', ('USD', 'btc', 'eth')


df = scrape_data()
## Sidebar - Cryptocurrency selections
sorted_coin = sorted( df['coin_symbol'] )
selected_coin = sid.multiselect('Cryptocurrency', sorted_coin, sorted_coin)

df_selected_coin = df[ (df['coin_symbol'].isin(selected_coin)) ] # Filtering data

## Sidebar - Number of coins to display
num_coin = sid.slider('Display Top N Coins', 1, 100, 50)
df_coins = df_selected_coin[:num_coin]
df_coins.drop(['percent_change_1h', 'percent_change_24h','percent_change_7d'], axis=1, inplace=True)
df_coins.rename({'rank' : '#', 'coin_name' : 'Name', 'coin_symbol' : 'Symbol', 'price' : 'Price',
					'market_cap' : 'Market Cap', 'volume_24h' : 'Volume (24h)'},axis=1, inplace=True)

col1.subheader('Price Data of Selected Cryptocurrency')
col1.write('Data Dimension: ' + str(df_selected_coin.shape[0]) + ' rows and ' + str(df_selected_coin.shape[1]) + ' columns.')

col1.dataframe(df_coins.assign(idx='').set_index('idx'))

# col1.dataframe(df.assign(idx='').set_index('idx'))

# Download CSV data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="crypto.csv">Download CSV File</a>'
    return href

col1.markdown(filedownload(df_selected_coin), unsafe_allow_html=True)

#---------------------------------#
# Preparing data for Bar plot of % Price change
col1.subheader('Table of % Price Change')
df_change = pd.concat([df.coin_name, df.coin_symbol, df.percent_change_1h, df.percent_change_24h, df.percent_change_7d], axis=1)
df_change = df_change.set_index('coin_symbol')
df_change['positive_percent_change_1h'] = df_change['percent_change_1h'] > 0
df_change['positive_percent_change_24h'] = df_change['percent_change_24h'] > 0
df_change['positive_percent_change_7d'] = df_change['percent_change_7d'] > 0
col1.dataframe(df_change)

# Conditional creation of Bar plot (time frame)
col2.subheader('Bar plot of % Price Change')

col3, col4 = st.beta_columns((1,1))
## Sidebar - Percent change timeframe
percent_timeframe = col2.selectbox('Percent change time frame',
                                    ['7d','24h', '1h'])
percent_dict = {"7d":'percent_change_7d',"24h":'percent_change_24h',"1h":'percent_change_1h'}
selected_percent_timeframe = percent_dict[percent_timeframe]

## Sidebar - Sorting values
sort_values = col2.selectbox('Sort values?', ['Yes', 'No'])


if percent_timeframe == '7d':
    if sort_values == 'Yes':
        df_change = df_change.sort_values(by=['percent_change_7d'])
    col2.write('*7 days period*')
    plt.figure(figsize=(5,25))
    plt.subplots_adjust(top = 1, bottom = 0)
    df_change['percent_change_7d'].plot(kind='barh', color=df_change.positive_percent_change_7d.map({True: 'g', False: 'r'}))
    col2.pyplot(plt)
elif percent_timeframe == '24h':
    if sort_values == 'Yes':
        df_change = df_change.sort_values(by=['percent_change_24h'])
    col2.write('*24 hour period*')
    plt.figure(figsize=(5,25))
    plt.subplots_adjust(top = 1, bottom = 0)
    df_change['percent_change_24h'].plot(kind='barh', color=df_change.positive_percent_change_24h.map({True: 'g', False: 'r'}))
    col2.pyplot(plt)
else:
    if sort_values == 'Yes':
        df_change = df_change.sort_values(by=['percent_change_1h'])
    col2.write('*1 hour period*')
    plt.figure(figsize=(5,25))
    plt.subplots_adjust(top = 1, bottom = 0)
    df_change['percent_change_1h'].plot(kind='barh', color=df_change.positive_percent_change_1h.map({True: 'g', False: 'r'}))
    col2.pyplot(plt)