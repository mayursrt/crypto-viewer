import streamlit as st
import pandas as pd
from PIL import Image
import base64
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests
import json
import time

# Set Page width
st.set_page_config(layout="wide")


# Logo
# image = Image.open('logo.jpg')
# st.image(image, width = 500)

# Title
st.title('Crypto Price App')
st.markdown("""
This app retrieves cryptocurrency prices for the top 100 cryptocurrency from the **CoinMarketCap**!
""")

# Page layout
sid = st.sidebar # Sidebar
col1, col2 = st.beta_columns((2,1)) # Main page

## SideBar



@st.cache
def scrape_data():
	cmc = requests.get('https://coinmarketcap.com/')
	soup = BeautifulSoup(cmc.content, 'html.parser')

	print(soup.title)

scrape_data()