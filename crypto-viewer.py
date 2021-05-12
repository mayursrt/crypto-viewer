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
## SideBar 

# currency_price_unit = col1.selectbox('Select currency for price', ('USD', 'btc', 'eth'))




df = scrape_data()
col1.dataframe(df.assign(idx='').set_index('idx'))