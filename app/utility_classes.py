import time
import datetime
import os

class PlaceLimitBuyOrder():
	def __init__(self, kraken_client, kraken_BTC_balance, \
		high_bid_0_kraken, high_bid_0_poloniex, high_bid_0_bittrex):
		self.currency = os.environ['currency']
		self.discount_to_average_bid = float(os.environ['kraken_discount_to_average_bid'])
		self.minimum_balance = float(os.environ['kraken_BTC_minimum_balance'])
		self.order_size = float(os.environ['kraken_BTC_order_size'])
		self.kraken_BTC_balance = kraken_BTC_balance
		self.high_bid_0_kraken = high_bid_0_kraken
		self.high_bid_0_poloniex = high_bid_0_poloniex
		self.high_bid_0_bittrex = high_bid_0_bittrex
		self.limit_bid_COIN = round(min(0.5*(self.high_bid_0_bittrex + self.high_bid_0_poloniex) \
			* (1 - self.discount_to_average_bid), self.high_bid_0_kraken + 0.00000001), int(os.environ['kraken_minimum_coin_order_size']))
		self.limit_buy_amount_COIN = min(self.order_size, self.kraken_BTC_balance)/self.limit_bid_COIN
		self.kraken_client = kraken_client

	def condition_1(self):
		if self.kraken_BTC_balance>self.minimum_balance:
			return True
		else:
			return False

	def action_1(self):
		orders = self.kraken_client.query_private('OpenOrders')['result']['open']
		for key in orders:
			if orders[key]['descr']['type'] == 'buy' and orders[key]['descr']['pair'] == os.environ['kraken_trading_pair']:
				try:
					cancelled_order = self.kraken_client.query_private('CancelOrder',{'txid':key})
				except Exception as e:
					print(e)
				else:
					continue
		limit_bid_COIN = '{:.8f}'.format(self.limit_bid_COIN)
		try:
			buy_order = self.kraken_client.query_private('AddOrder',{'pair': os.environ['kraken_trading_pair'],'type':'buy','ordertype':'limit',\
				'price':limit_bid_COIN,'volume':self.limit_buy_amount_COIN})
			if buy_order == {'error':['EOrder:Insufficient funds']}:
				raise InsufficientFundsError
			if buy_order == {'error':['EGeneral:Invalid arguments:volume']}:
				raise InsufficientVolumeError
		except Exception as e:
				print(e)
		finally:
			time.sleep(5)

	def execute(self):
		if self.condition_1():
			self.action_1()

class PlaceLimitSellOrder():
	def __init__(self, kraken_client, kraken_COIN_balance, \
		low_ask_0_bittrex, low_ask_0_poloniex, low_ask_0_kraken):
		self.currency = os.environ['currency']
		self.kraken_COIN_balance = kraken_COIN_balance
		self.premium_to_average_ask = float(os.environ['kraken_premium_to_average_ask'])
		self.minimum_balance = 0
		self.order_size = self.kraken_COIN_balance
		self.low_ask_0_bittrex = low_ask_0_bittrex
		self.low_ask_0_poloniex = low_ask_0_poloniex
		self.low_ask_0_kraken = low_ask_0_kraken
		self.limit_ask_COIN = round(max(0.5*(self.low_ask_0_bittrex+self.low_ask_0_poloniex)\
			*(1.0+self.premium_to_average_ask),(self.low_ask_0_kraken-0.00000001)), int(os.environ['kraken_limit_ask_COIN']))
		self.limit_sell_amount_COIN = min(self.order_size,self.kraken_COIN_balance)
		self.kraken_client = kraken_client

	def condition_1(self):
		if self.kraken_COIN_balance>self.minimum_balance:
			return True
		else:
			return False

	def action_1(self):
		orders = self.kraken_client.query_private('OpenOrders')['result']['open']
		for key in orders:
			if orders[key]['descr']['type'] == 'sell' and orders[key]['descr']['pair'] == os.environ['kraken_trading_pair']:
				try:
					cancelled_order = self.kraken_client.query_private('CancelOrder',{'txid':key})
				except Exception as e:
					print(e)
				else:
					continue
		limit_ask_COIN = '{:.8f}'.format(self.limit_ask_COIN)
		try:
			sell_order = self.kraken_COIN_balance, self.kraken_client.query_private('AddOrder',{'pair': os.environ['kraken_trading_pair'],'type':'sell','ordertype':'limit',\
				'price':limit_ask_COIN,'volume':self.limit_sell_amount_COIN})
			if sell_order[1] == {'error':['EGeneral:Invalid arguments:volume']}:
				raise InsufficientVolumeError
		except Exception as e:
				print(e)
		finally:
			time.sleep(5)

	def execute(self):
		if self.condition_1():
			self.action_1()

class Error(Exception):
   """Base class for other exceptions"""
   pass
class InsufficientVolumeError(Error):
   """Raised when the volume amount is too small"""
   pass

class InsufficientFundsError(Error):
	"""Raised when the buy order does not have sufficient funds"""
	pass