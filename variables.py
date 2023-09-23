import kraken.api as kraken
import poloniex.__init__ as poloniex
import bittrex.bittrex as bittrex
import asyncio

def get_prices_volumes(kraken, poloniex, bittrex, currency):
	
	loop = asyncio.new_event_loop()
	task_kraken = loop.create_task(get_kraken_price_volume(kraken, currency))
	task_poloniex = loop.create_task(get_poloniex_price_volume(poloniex, currency))
	task_bittrex = loop.create_task(get_bittrex_price_volume(bittrex, currency))
	loop.run_until_complete(asyncio.wait([task_kraken,task_poloniex,task_bittrex]))
	loop.close()

	high_bid_0_kraken, low_ask_0_kraken = task_kraken.result()
	high_bid_0_poloniex, low_ask_0_poloniex = task_poloniex.result()
	high_bid_0_bittrex, low_ask_0_bittrex = task_bittrex.result()

	return high_bid_0_kraken, low_ask_0_kraken, high_bid_0_poloniex, \
	low_ask_0_poloniex, high_bid_0_bittrex, low_ask_0_bittrex

def calculate_balances(kraken, currency):

	#kraken
	kraken_balance_data = kraken.query_private('Balance')['result']
	try:
		kraken_balance = float(kraken_balance_data[{'BITCOIN':'XXBT','RIPPLE':'XXRP','ETC_CLASSIC':'XETC',\
			'ATOM':'ATOM','MONERO':'XXMR','DASH':'DASH','STELLAR':'XXLM'}[currency]])
		kraken_BTC_balance = float(kraken_balance_data['XXBT'])
	except:
		kraken_balance = 0
		kraken_BTC_balance = 0

	return kraken_BTC_balance, kraken_balance

async def get_kraken_price_volume(kraken, currency):
	
	await asyncio.sleep(0)
	kraken_price_volume_data = kraken.query_public('Depth',{'pair':{'DOGE':'XDGXBT','RIPPLE':'XRPXBT',\
		'BITCOIN':'XBTUSD','ETC_CLASSIC':'ETCXBT','ATOM':'ATOMXBT','MONERO':'XMRXBT','DASH':'DASHXBT','STELLAR':'XLMXBT'}[currency],'count':15})\
	['result'][{'DOGE':'XXDGXXBT','RIPPLE':'XXRPXXBT','BITCOIN':'XXBTZUSD',\
	'ETC_CLASSIC':'XETCXXBT','ATOM':'ATOMXBT','MONERO':'XXMRXXBT','DASH':'DASHXBT','STELLAR':'XXLMXXBT'}[currency]]
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

async def get_poloniex_price_volume(poloniex, currency):

	await asyncio.sleep(0)
	poloniex_price_volume_data = poloniex.returnOrderBook({'DOGE':'BTC_DOGE','BITCOIN':'USDC_BTC','RIPPLE':'BTC_XRP',\
		'ETC_CLASSIC':'BTC_ETC','ATOM':'BTC_ATOM','MONERO':'BTC_XMR','DASH':'BTC_DASH','STELLAR':'BTC_STR'}[currency])
	high_bid_0_poloniex = float(poloniex_price_volume_data['bids'][0][0])
	low_ask_0_poloniex = float(poloniex_price_volume_data['asks'][0][0])

	return high_bid_0_poloniex, low_ask_0_poloniex

async def get_bittrex_price_volume(bittrex, currency):

	await asyncio.sleep(0)
	bittrex_price_volume_data = bittrex.get_orderbook({'RIPPLE':'BTC-XRP','BITCOIN':'USD-BTC','DOGE':'BTC-XRP',\
		'ETC_CLASSIC':'BTC-ETC','ATOM':'BTC-ATOM','MONERO':'BTC-XMR','DASH':'BTC-DASH','STELLAR':'BTC-XLM'}[currency])['result']
	high_bid_0_bittrex = bittrex_price_volume_data['buy'][0]['Rate']
	low_ask_0_bittrex = bittrex_price_volume_data['sell'][0]['Rate']

	return high_bid_0_bittrex, low_ask_0_bittrex