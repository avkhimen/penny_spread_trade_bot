import time
import datetime
import random
from support_functions import get_timestamp_from_unix

class PlaceLimitBuyOrder():
	def __init__(self, currency, kraken, kraken_BTC_balance, \
		high_bid_0_kraken, high_bid_0_poloniex, high_bid_0_bittrex, session):
		self.currency = currency
		self.discount_to_average_bid = {'DOGE':0.0125,'RIPPLE':0.0125,'BITCOIN':0.0075,\
		'ETC_CLASSIC':0.02,'ATOM':0.015,'MONERO':0.0125,'DASH':0.0125,'STELLAR':0.0125}[self.currency]
		self.minimum_balance = {'DOGE':0.05,'RIPPLE':0.05,'BITCOIN':0.05,'ETC_CLASSIC':0.05,\
		'ATOM':0.05,'MONERO':0.05,'DASH':0.05,'STELLAR':0.05}[self.currency]
		self.order_size = {'DOGE':0.05,'RIPPLE':0.05,'BITCOIN':0.05,'ETC_CLASSIC':0.05,\
		'ATOM':0.05,'MONERO':0.05,'MONERO':0.05,'DASH':0.05,'STELLAR':0.05}[self.currency]
		self.kraken_BTC_balance = kraken_BTC_balance
		self.high_bid_0_kraken = high_bid_0_kraken
		self.high_bid_0_poloniex = high_bid_0_poloniex
		self.high_bid_0_bittrex = high_bid_0_bittrex
		self.limit_bid_COIN = round(min(0.5*(self.high_bid_0_bittrex + self.high_bid_0_poloniex) \
			* (1 - self.discount_to_average_bid), self.high_bid_0_kraken + 0.00000001), {'DOGE':8,'RIPPLE':8,'BITCOIN':8,'ETC_CLASSIC':6,\
		'ATOM':7,'MONERO':6,'DASH':5,'STELLAR':8}[self.currency])
		self.limit_buy_amount_COIN = min(self.order_size, self.kraken_BTC_balance)/self.limit_bid_COIN
		self.kraken = kraken
		self.session = session

	def condition_1(self):
		if self.kraken_BTC_balance>self.minimum_balance:
			return True
		else:
			return False

	def action_1(self):
		orders = self.kraken.query_private('OpenOrders')['result']['open']
		for key in orders:
			if orders[key]['descr']['type'] == 'buy' and orders[key]['descr']['pair'] == {'DOGE':'XDGXBT',\
			'RIPPLE':'XRPXBT','BITCOIN':'XBTUSD','ETC_CLASSIC':'ETCXBT','ATOM':'ATOMXBT',\
			'MONERO':'XMRXBT','DASH':'DASHXBT','STELLAR':'XLMXBT'}[self.currency]:
				try:
					cancelled_order = self.kraken.query_private('CancelOrder',{'txid':key})
					if cancelled_order['result']['count'] == 1:
						RecordCancelledOrders(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), \
							key, self.currency, self.session, "buy").create_record()
				except Exception as e:
					print(e)
				else:
					continue
		limit_bid_COIN = '{:.8f}'.format(self.limit_bid_COIN)
		try:
			buy_order = self.kraken.query_private('AddOrder',{'pair':{'DOGE':'XDGXBT','RIPPLE':'XRPXBT','BITCOIN':'XBTUSD',\
				'ETC_CLASSIC':'ETCXBT','ATOM':'ATOMXBT','MONERO':'XMRXBT',\
				'DASH':'DASHXBT','STELLAR':'XLMXBT'}[self.currency],'type':'buy','ordertype':'limit',\
				'price':limit_bid_COIN,'volume':self.limit_buy_amount_COIN})
			if buy_order == {'error':['EOrder:Insufficient funds']}:
				raise InsufficientFundsError
			if buy_order == {'error':['EGeneral:Invalid arguments:volume']}:
				raise InsufficientVolumeError
			if buy_order['result']['txid'][0] != "":
				RecordPlacedOrders(buy_order['result']['txid'][0], datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), \
					"buy", "limit", limit_bid_COIN, self.limit_buy_amount_COIN, self.currency, self.session).create_record()
		except Exception as e:
				print(e)
		finally:
			time.sleep(5)

	def execute(self):
		if self.condition_1():
			self.action_1()

class PlaceLimitSellOrder():
	def __init__(self, currency, kraken, kraken_COIN_balance, \
		low_ask_0_bittrex, low_ask_0_poloniex, low_ask_0_kraken, session):
		self.currency = currency
		self.kraken_COIN_balance = kraken_COIN_balance
		self.premium_to_average_ask = {'DOGE':0.0075,'RIPPLE':0.0035,'BITCOIN':0.0075,'ETC_CLASSIC':0.005,\
		'ATOM':0.004,'MONERO':0.0035,'DASH':0.0035,'STELLAR':0.0035}[self.currency]
		self.minimum_balance = {'DOGE':0,'RIPPLE':0,'BITCOIN':0,'ETC_CLASSIC':0,\
		'ATOM':0,'MONERO':0,'DASH':0,'STELLAR':0}[self.currency]
		self.order_size = {'DOGE':400,'RIPPLE':self.kraken_COIN_balance,'BITCOIN':400,'ETC_CLASSIC':self.kraken_COIN_balance,\
		'ATOM':self.kraken_COIN_balance,'MONERO':self.kraken_COIN_balance,'DASH':self.kraken_COIN_balance,\
		'STELLAR':self.kraken_COIN_balance}[self.currency]
		self.low_ask_0_bittrex = low_ask_0_bittrex
		self.low_ask_0_poloniex = low_ask_0_poloniex
		self.low_ask_0_kraken = low_ask_0_kraken
		self.limit_ask_COIN = round(max(0.5*(self.low_ask_0_bittrex+self.low_ask_0_poloniex)\
			*(1.0+self.premium_to_average_ask),(self.low_ask_0_kraken-0.00000001)),{'DOGE':8,'RIPPLE':8,'BITCOIN':8,\
		'ETC_CLASSIC':6,'ATOM':7,'MONERO':6,'MONERO':6,'DASH':5,'STELLAR':8}[self.currency])
		self.limit_sell_amount_COIN = min(self.order_size,self.kraken_COIN_balance)
		self.kraken = kraken
		self.session = session

	def condition_1(self):
		if self.kraken_COIN_balance>self.minimum_balance:
			return True
		else:
			return False

	def action_1(self):
		orders = self.kraken.query_private('OpenOrders')['result']['open']
		for key in orders:
			if orders[key]['descr']['type'] == 'sell' and orders[key]['descr']['pair'] == {'DOGE':'XDGXBT','RIPPLE':'XRPXBT',\
			'BITCOIN':'XBTUSD','ETC_CLASSIC':'ETCXBT','ATOM':'ATOMXBT','MONERO':'XMRXBT',\
			'DASH':'DASHXBT','STELLAR':'XLMXBT'}[self.currency]:
				try:
					cancelled_order = self.kraken.query_private('CancelOrder',{'txid':key})
					if cancelled_order['result']['count'] == 1:
						RecordCancelledOrders(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), \
							key, self.currency, self.session, "sell").create_record()
				except Exception as e:
					print(e)
				else:
					continue
		limit_ask_COIN = '{:.8f}'.format(self.limit_ask_COIN)
		try:
			sell_order = self.kraken_COIN_balance, self.kraken.query_private('AddOrder',{'pair':{'DOGE':'XDGXBT','RIPPLE':'XRPXBT','BITCOIN':'XBTUSD',\
				'ETC_CLASSIC':'ETCXBT','ATOM':'ATOMXBT','MONERO':'XMRXBT','DASH':'DASHXBT',\
				'STELLAR':'XLMXBT'}[self.currency],'type':'sell','ordertype':'limit',\
				'price':limit_ask_COIN,'volume':self.limit_sell_amount_COIN})
			if sell_order[1] == {'error':['EGeneral:Invalid arguments:volume']}:
				raise InsufficientVolumeError
			if isinstance(sell_order, tuple) and sell_order[1]['result']['txid'][0] != "":
				RecordPlacedOrders(sell_order[1]['result']['txid'][0], datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), \
					"sell", "limit", limit_ask_COIN, self.limit_sell_amount_COIN, self.currency, self.session).create_record()
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