#---------------------------------------------------------------------------------------------------
# Imports

import streamlit as st
import pandas as pd
from PIL import Image
import base64
import matplotlib.pyplot as plt
from scrape_data import *
#---------------------------------------------------------------------------------------------------


# Set Page width
st.set_page_config(layout="wide")


# Logo
# image = Image.open('logo.jpg')
# st.image(image, width = 500)

#---------------------------------------------------------------------------------------------------
# Title

title_container = st.beta_container()
col1, col2 = st.beta_columns([1, 5])
image = Image.open('assets/logo.jpg')
with title_container:
    with col1:
        st.image(image)
    with col2:
        st.title('Crypto Price App')
        st.markdown("""
This app retrieves cryptocurrency prices for the top 100 cryptocurrency from the **CoinMarketCap**!

-by Mayur Machhi
""")




#---------------------------------------------------------------------------------------------------
# Page layout
sid = st.sidebar # Sidebar
# st, st = st.beta_columns((2,1)) # Main page


# currency_price_unit = st.selectbox('Select currency for price', ('USD', 'btc', 'eth')


df = scrape_data()

## Sidebar - Number of coins to display
num_coin = sid.slider('Display Top N Coins', 1, 100, 100)


## Sidebar - Cryptocurrency selections
sorted_coin = sorted( df['coin_symbol'] )
selected_coin = sid.multiselect('Cryptocurrency', sorted_coin, sorted_coin)

df_selected_coin = df[ (df['coin_symbol'].isin(selected_coin)) ] # Filtering data


df_coins = df_selected_coin[:num_coin]

# df_coins['coin_name'] = df_coins['coin_name'].map(str) + '(' + df_coins['coin_symbol'] + ')'
df_coins.drop(['percent_change_1h', 'percent_change_24h','percent_change_7d'], axis=1, inplace=True)
df_coins.rename({'rank' : '#', 'coin_name' : 'Name', 'coin_symbol' : 'Symbol', 'price' : 'Price',
					'market_cap' : 'Market Cap', 'volume_24h' : 'Volume (24h)'},axis=1, inplace=True)


df_coins = df_coins.set_index('#')
#---------------------------------------------------------------------------------------------------
# Coins Dataframe
st.markdown(f'## **Price Data of Top {num_coin} Cryptocurrencies.**')
st.dataframe(df_coins.style.format({'Price': '{0:,.3f} $', 'Market Cap': '{0:,.0f} $', 'Volume (24h)': '{0:,.0f} $'}))
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

#---------------------------------------------------------------------------------------------------
# Percent change timeframe
st.markdown('## **Price Changes**')

col1, col2, col3, col4 = st.beta_columns((2,2,2,3))
percent_timeframe = col1.selectbox('Percent change time frame',
                                    ['7d','24h', '1h'])
top_bottom = col3.selectbox('Top/Bottom n Changes', [5,10,15])
col4.empty()

percent_dict = {"7d":'percent_change_7d',"24h":'percent_change_24h',"1h":'percent_change_1h'}
selected_percent_timeframe = percent_dict[percent_timeframe]

## Sidebar - Sorting values
sort_values = col2.selectbox('Sort values?', ['Yes', 'No'])
#---------------------------------------------------------------------------------------------------


st.markdown(f'*{percent_timeframe} period*')


#---------------------------------------------------------------------------------------------------
## Top/ Bottom n changes
col1, col2 = st.beta_columns((1,1))
col1.subheader(f'Top {top_bottom} Gainers')
col1.empty()
col2.subheader(f'Top {top_bottom} Losers')
col2.empty()

col1, col2, col3, col4 = st.beta_columns((1,0.5,1,0.5))

top_n = df_change[df_change[selected_percent_timeframe] > 0]
top_n = top_n.sort_values(by=[selected_percent_timeframe], ascending=False)

if top_n.empty == False:
	top_n_show = top_n[['coin_name', selected_percent_timeframe]][:top_bottom]
	top_n_show = top_n_show.rename({'coin_name' : 'Name'}, axis=1)
	col1.dataframe(top_n_show.style.set_properties(**{'color': 'green'}, subset=[selected_percent_timeframe]).format({selected_percent_timeframe : '+{0:,.3f}%'}))


	plt.figure(figsize=(3,2))
	plt.subplots_adjust(top = 1, bottom = 0)
	plt.xlabel('Coin Symbol')
	plt.ylabel('Price')
	top_n[selected_percent_timeframe][:top_bottom].plot(kind='bar', color=top_n['positive_'+selected_percent_timeframe].map({True: 'g', False: 'r'}))
	col2.pyplot(plt)
else:
	col1.markdown(f'No Gainers for selected Timeframe')

bottom_n = df_change[df_change[selected_percent_timeframe] < 0]
bottom_n = bottom_n.sort_values(by=[selected_percent_timeframe])

if bottom_n.empty == False:

	bottom_n_show = bottom_n[['coin_name', selected_percent_timeframe]][:top_bottom]
	bottom_n_show = bottom_n_show.rename({'coin_name' : 'Name'}, axis=1)
	col3.dataframe(bottom_n_show.style.set_properties(**{'color': 'red'}, subset=[selected_percent_timeframe]).format({selected_percent_timeframe : '{0:,.3f}%'}))

	plt.figure(figsize=(3,2))
	plt.subplots_adjust(top = 1, bottom = 0)
	plt.xlabel('Coin Symbol')
	plt.ylabel('Price')
	bottom_n[selected_percent_timeframe][:top_bottom].plot(kind='bar', color=bottom_n['positive_'+selected_percent_timeframe].map({True: 'g', False: 'r'}))
	col4.pyplot(plt)
else:
	col3.markdown('No Losers for selected Timeframe')
#---------------------------------------------------------------------------------------------------



#---------------------------------------------------------------------------------------------------
# % Change Bar Plot
st.subheader('Bar plot of % Price Change')

if sort_values == 'Yes':
    df_change = df_change.sort_values(by=[selected_percent_timeframe], ascending=False)
plt.figure(figsize=(25,4))
plt.subplots_adjust(top = 1, bottom = 0)
plt.xlabel('Coin Symbol')
plt.ylabel('Price')
df_change[selected_percent_timeframe].plot(kind='bar', color=df_change['positive_'+selected_percent_timeframe].map({True: 'g', False: 'r'}))
st.pyplot(plt)
#---------------------------------------------------------------------------------------------------



#---------------------------------------------------------------------------------------------------
# Change Dataframe
st.subheader('Table of % Price Change')

def color(val):
    if val < 0:
        c = 'red'
    elif val > 0:
        c = 'green'
    else:
        c = 'yellow'
    return 'color: %s' % c


st.dataframe(df_change_show.style.applymap(color, subset=['Percent Change (1h)', 'Percent Change (24h)', 'Percent Change (7d)']).
	format({'Percent Change (1h)': '{:.2f}%', 'Percent Change (24h)': '{:.2f}%', 'Percent Change (7d)': '{:.2f}%'}))
#---------------------------------------------------------------------------------------------------



# col3.dataframe(bottom_n_show.style.set_properties(**{'color': 'red'}, subset=[selected_percent_timeframe]))



#----------------------------------------------------------------------------------------------------------------------------
#Footer

footer="""<style>
#MainMenu {visibility: hidden;}
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: black;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: white;
color: black;
text-align: center;
}
</style>
<div class="footer">
<p>Made in Streamlit with ❤️ by <a href='https://github.com/mayursrt'>Mayur</a> 

</p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)

# <a style='display: block; text-align: center;' href="https://github.com/mayursrt" target="_blank">Mayur Machhi</a>

#----------------------------------------------------------------------------------------------------------------------------