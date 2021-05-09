import streamlit as st
import pandas as pd
from PIL import Image
import base64
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests
import json
import time


@st.cache
def scrape_data():
	cmc = requests.get('https://coinmarketcap.com/')
	soup = BeautifulSoup(cmc.content, 'html.parser')

	print(soup.title)