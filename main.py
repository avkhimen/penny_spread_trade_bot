from utility_classes import PlaceLimitBuyOrder, PlaceLimitSellOrder
from utility_classes import RecordPrices, RecordBalances, RecordFilledOrders
import kraken.api as kraken
import poloniex.__init__ as poloniex
import bittrex.bittrex as bittrex
from support_functions import get_input_args
from variables import get_prices_volumes, calculate_balances
from initialize_accounts import initialize_accounts
import time
import datetime

def main():
	currency = get_input_args().currency_pair
	kraken, poloniex, bittrex = initialize_accounts()

	while True:
		try:
			print('##################################################################### iteration #' \
				'{} #####################################################################'.format(i))
			i += 1

			print('Calculating balances')
			kraken_BTC_balance, kraken_balance = calculate_balances(kraken, poloniex, bittrex, currency)
			print('kraken_BTC_balance is {} and kraken_{}_balance is {}'.format(kraken_BTC_balance, currency, kraken_balance))

			print('Recording balances')
			RecordBalances(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),\
				kraken_balance, kraken_BTC_balance, currency, session).create_record()

			print('Calculating prices')
			high_bid_0_kraken, low_ask_0_kraken, high_bid_0_poloniex, \
			low_ask_0_poloniex, high_bid_0_bittrex, low_ask_0_bittrex = get_prices_volumes(kraken, poloniex, bittrex, currency)
			print('Prices calculated')

			print('Cancelling existing buy order and placing new buy order')
			PlaceLimitBuyOrder(currency, kraken,\
				kraken_BTC_balance, high_bid_0_kraken, high_bid_0_poloniex, high_bid_0_bittrex, session).execute()

			print('Recording prices')
			RecordPrices(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),\
				high_bid_0_kraken, low_ask_0_kraken, high_bid_0_poloniex, \
			low_ask_0_poloniex, high_bid_0_bittrex, low_ask_0_bittrex, currency, session).create_record()

			print('Calculating balances')
			kraken_BTC_balance, kraken_balance = calculate_balances(kraken, poloniex, bittrex, currency)
			print('kraken_BTC_balance is {} and kraken_balance is {}'.format(kraken_BTC_balance, kraken_balance))

			print('Recording balances')
			RecordBalances(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),\
				kraken_balance, kraken_BTC_balance, currency, session).create_record()

			print('Calculating prices')
			high_bid_0_kraken, low_ask_0_kraken, high_bid_0_poloniex, \
			low_ask_0_poloniex, high_bid_0_bittrex, low_ask_0_bittrex = get_prices_volumes(kraken, poloniex, bittrex, currency)
			print('Prices calculated')

			print('Cancelling existing sell order and placing new sell order')
			PlaceLimitSellOrder(currency, kraken,\
				kraken_balance, low_ask_0_bittrex, low_ask_0_poloniex, low_ask_0_kraken, session).execute()

			print('Recording prices')
			RecordPrices(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),\
				high_bid_0_kraken, low_ask_0_kraken, high_bid_0_poloniex, \
			low_ask_0_poloniex, high_bid_0_bittrex, low_ask_0_bittrex, currency, session).create_record()

			print("Timestamp: {} Kraken {} Balance: {} Kraken BTC Balance: {} Kraken price: {} Poloniex price: {} Bittrex price: {}"\
				.format(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), currency, \
				kraken_balance, kraken_BTC_balance, high_bid_0_kraken, high_bid_0_poloniex, high_bid_0_bittrex))

			print('Recording filled orders')
			RecordFilledOrders(kraken, currency, session).create_record()

			time.sleep(10)
		except Exception as e:
			print(e)

if __name__ == "__main__":
	main()