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
# st, st = st.beta_columns((2,1)) # Main page


# currency_price_unit = st.selectbox('Select currency for price', ('USD', 'btc', 'eth')


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

st.subheader('Price Data of Selected Cryptocurrency')
st.write('Data Dimension: ' + str(df_selected_coin.shape[0]) + ' rows and ' + str(df_selected_coin.shape[1]) + ' columns.')
df_coins = df_coins.set_index('#')
#---------------------------------------------------------------------------------------------------
# Coins Dataframe
st.dataframe(df_coins)
#---------------------------------------------------------------------------------------------------

st.markdown(filedownload(df_selected_coin), unsafe_allow_html=True)

# Preparing data for Bar plot of % Price change

df_change = pd.concat([df.coin_name, df.coin_symbol, df.percent_change_1h, df.percent_change_24h, df.percent_change_7d], axis=1)
df_change.rename({'coin_symbol' : 'Coin Symbol'}, axis=1, inplace=True)
df_change = df_change.set_index('Coin Symbol')
df_change['positive_percent_change_1h'] = df_change['percent_change_1h'] > 0
df_change['positive_percent_change_24h'] = df_change['percent_change_24h'] > 0
df_change['positive_percent_change_7d'] = df_change['percent_change_7d'] > 0
df_change = df_change[:num_coin]
df_change_show = df_change.drop(['positive_percent_change_7d', 'positive_percent_change_24h', 'positive_percent_change_1h'], axis=1)
df_change_show.rename({'coin_name' : 'Name', 'coin_symbol' : 'Symbol', 'percent_change_1h' : 'Percent Change (1h)', 
					'percent_change_24h' : 'Percent Change (24h)', 'percent_change_7d' : 'Percent Change (7d)'}, axis=1, inplace=True)

# Conditional creation of Bar plot (time frame)
st.subheader('Bar plot of % Price Change')

## Sidebar - Percent change timeframe
col1, col2, col3 = st.beta_columns((2,2,5))
percent_timeframe = col1.selectbox('Percent change time frame',
                                    ['7d','24h', '1h'])
col3.empty()

percent_dict = {"7d":'percent_change_7d',"24h":'percent_change_24h',"1h":'percent_change_1h'}
selected_percent_timeframe = percent_dict[percent_timeframe]

## Sidebar - Sorting values
sort_values = col2.selectbox('Sort values?', ['Yes', 'No'])

#---------------------------------------------------------------------------------------------------
# % Change Bar Plot
if percent_timeframe == '7d':
    if sort_values == 'Yes':
        df_change = df_change.sort_values(by=['percent_change_7d'])
    st.write('*7 days period*')
    plt.figure(figsize=(25,5))
    plt.subplots_adjust(top = 1, bottom = 0)
    plt.xlabel('Coin Symbol')
    plt.ylabel('Price')
    df_change['percent_change_7d'].plot(kind='bar', color=df_change.positive_percent_change_7d.map({True: 'g', False: 'r'}))
    st.pyplot(plt)
elif percent_timeframe == '24h':
    if sort_values == 'Yes':
        df_change = df_change.sort_values(by=['percent_change_24h'])
    st.write('*24 hour period*')
    plt.figure(figsize=(25,5))
    plt.subplots_adjust(top = 1, bottom = 0)
    plt.xlabel('Coin Symbol')
    plt.ylabel('Price')
    df_change['percent_change_24h'].plot(kind='bar', color=df_change.positive_percent_change_24h.map({True: 'g', False: 'r'}))
    st.pyplot(plt)
else:
    if sort_values == 'Yes':
        df_change = df_change.sort_values(by=['percent_change_1h'])
    st.write('*1 hour period*')
    plt.figure(figsize=(25,5))
    plt.subplots_adjust(top = 1, bottom = 0)
    plt.xlabel('Coin Symbol')
    plt.ylabel('Price')
    df_change['percent_change_1h'].plot(kind='bar', color=df_change.positive_percent_change_1h.map({True: 'g', False: 'r'}))
    st.pyplot(plt)
#---------------------------------------------------------------------------------------------------

st.subheader('Table of % Price Change')
#---------------------------------------------------------------------------------------------------
# Change Dataframe
st.dataframe(df_change_show)
#---------------------------------------------------------------------------------------------------



#---------------------------------------------------------------------------------------------------
col1, col2 = st.beta_columns((1,1))

top_n = df_change[df_change['positive_percent_change_7d'] == 1]
top_n = top_n.sort_values(by=['percent_change_7d', 'positive_percent_change_7d'], ascending=False)

plt.figure(figsize=(5,3))
#plt.subplots_adjust(top = 1, bottom = 0)
plt.xlabel('Coin Symbol')
plt.ylabel('Price')
top_n['percent_change_7d'][:5].plot(kind='bar', color=top_n.positive_percent_change_7d.map({True: 'g', False: 'r'}))
col1.pyplot(plt)

bottom_n = df_change[df_change['positive_percent_change_7d'] == 0]
bottom_n = bottom_n.sort_values(by=['percent_change_7d', 'positive_percent_change_7d'])

plt.figure(figsize=(5,3))
#plt.subplots_adjust(top = 1, bottom = 0)
plt.xlabel('Coin Symbol')
plt.ylabel('Price')
bottom_n['percent_change_7d'][:5].plot(kind='bar', color=bottom_n.positive_percent_change_7d.map({True: 'g', False: 'r'}))
col2.pyplot(plt)



#---------------------------------------------------------------------------------------------------