import kraken.api as kraken
import os
import requests

def get_prices_volumes(kraken_client):

	high_bid_0_kraken, low_ask_0_kraken = get_kraken_price_volume(kraken_client)
	high_bid_0_poloniex, low_ask_0_poloniex = get_poloniex_price_volume()
	#high_bid_0_bittrex, low_ask_0_bittrex = get_bittrex_price_volume()
	high_bid_0_bittrex, low_ask_0_bittrex = get_bitfinex_price_volume()

	return high_bid_0_kraken, low_ask_0_kraken, high_bid_0_poloniex, \
	low_ask_0_poloniex, high_bid_0_bittrex, low_ask_0_bittrex

def calculate_balances(kraken_client):

	#kraken
	kraken_balance_data = kraken_client.query_private('Balance')['result']
	try:
		kraken_balance = float(kraken_balance_data[os.environ['coin_balance_ticker']])
		kraken_BTC_balance = float(kraken_balance_data['XXBT'])
	except Exception as e:
		kraken_balance = 0
		kraken_BTC_balance = 0

	return kraken_BTC_balance, kraken_balance

def get_kraken_price_volume(kraken_client):
	
	kraken_price_volume_data = kraken_client.query_public('Depth',{'pair': os.environ['kraken_trading_pair'],'count':15})\
	['result'][os.environ['kraken_price_volume_result_trading_pair']]
	cumulative_sum = 0
	i = 0
	cumulative_sum += float(kraken_price_volume_data['bids'][i][1])
	while cumulative_sum * float(kraken_price_volume_data['bids'][i][0]) <= 0.1:
		i+=1
		cumulative_sum += float(kraken_price_volume_data['bids'][i][1])
	high_bid_0_kraken = float(kraken_price_volume_data['bids'][i][0])
	cumulative_sum = 0
	i = 0
	cumulative_sum += float(kraken_price_volume_data['asks'][i][1])
	while cumulative_sum * float(kraken_price_volume_data['asks'][i][0]) <= 0.1:
		i+=1
		cumulative_sum += float(kraken_price_volume_data['asks'][i][1])
	low_ask_0_kraken = float(kraken_price_volume_data['asks'][i][0])

	return high_bid_0_kraken, low_ask_0_kraken

def get_poloniex_price_volume():

	poloniex_price_volume_data = requests.get(f"https://api.poloniex.com/markets/{os.environ['poloniex_trading_pair']}/orderBook").json()
	high_bid_0_poloniex = float(poloniex_price_volume_data['bids'][0])
	low_ask_0_poloniex = float(poloniex_price_volume_data['asks'][0])

	return high_bid_0_poloniex, low_ask_0_poloniex

def get_bittrex_price_volume():

	bittrex_price_volume_data = requests.get(f"https://api.bittrex.com/v3/markets/{os.environ['bittrex_trading_pair']}/orderbook").json()
	high_bid_0_bittrex = float(bittrex_price_volume_data['bid'][0]['rate'])
	low_ask_0_bittrex = float(bittrex_price_volume_data['ask'][0]['rate'])

	return high_bid_0_bittrex, low_ask_0_bittrex

def get_bitfinex_price_volume():

	bitfinex_price_volume_data = requests.get(f"https://api.bitfinex.com/v1/book/{os.environ['bitfinex_trading_pair']}").json()
	high_bid_0_bitfinex = float(bittrex_price_volume_data['bids'][0]['price'])
	low_ask_0_bitfinex = float(bittrex_price_volume_data['asks'][0]['price'])

	return high_bid_0_bitfinex, low_ask_0_bitfinex