import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
import requests
import json
import time

@st.cache
def scrape_data():
  cmc = requests.get('https://coinmarketcap.com/')
  soup = BeautifulSoup(cmc.content, 'html.parser')

  data = soup.find('script', id='__NEXT_DATA__', type='application/json')
  coins = {}
  data.contents[0]
  coin_data = json.loads(data.contents[0])
  listings = coin_data['props']['initialState']['cryptocurrency']['listingLatest']['data']

  for i in listings:
    coins[str(i['id'])] = i['slug']


  coin_name = []
  coin_rank = []
  coin_symbol = []
  market_cap = []
  percent_change_1h = []
  percent_change_24h = []
  percent_change_7d = []
  price = []
  volume_24h = []

  for i in listings:
    coin_name.append(i['name'])
    coin_rank.append(i['rank'])
    coin_symbol.append(i['symbol'])
    price.append(i['quote']['USD']['price'])
    percent_change_1h.append(i['quote']['USD']['percentChange1h'])
    percent_change_24h.append(i['quote']['USD']['percentChange24h'])
    percent_change_7d.append(i['quote']['USD']['percentChange7d'])
    market_cap.append(i['quote']['USD']['marketCap'])
    volume_24h.append(i['quote']['USD']['volume24h'])


  df = pd.DataFrame(columns=['coin_rank','coin_name', 'coin_symbol','price', 'market_cap', 'percent_change_1h', 'percent_change_24h', 'percent_change_7d', 'volume_24h'])
  df['coin_rank'] = coin_rank
  df['coin_name'] = coin_name
  df['coin_symbol'] = coin_symbol
  df['price'] = price
  df['percent_change_1h'] = percent_change_1h
  df['percent_change_24h'] = percent_change_24h
  df['percent_change_7d'] = percent_change_7d
  df['market_cap'] = market_cap
  df['volume_24h'] = volume_24h
  return df
