from utility_classes import PlaceLimitBuyOrder, PlaceLimitSellOrder
import kraken.api as kraken
from support_functions import get_input_args
from volumes_balances import get_prices_volumes, calculate_balances
from initialize_accounts import initialize_accounts
import time
import datetime
import os
import logging

logging.getLogger().setLevel(logging.INFO)

def main():
	
	#currency = get_input_args().currency_pair
	currency = os.environ['currency']
	#kraken, poloniex, bittrex = initialize_accounts()
	kraken_client = initialize_accounts()

	while True:
		try:

			kraken_BTC_balance, kraken_balance = calculate_balances(kraken_client)

			logging.info(kraken_BTC_balance, kraken_balance)

			logging.info('Calculating prices')
			high_bid_0_kraken, low_ask_0_kraken, high_bid_0_poloniex, low_ask_0_poloniex, high_bid_0_bittrex, low_ask_0_bittrex = get_prices_volumes(kraken_client)

			logging.info('Cancelling existing buy order and placing new buy order')
			PlaceLimitBuyOrder(kraken_client, kraken_BTC_balance, high_bid_0_kraken, high_bid_0_poloniex, high_bid_0_bittrex).execute()

			logging.info('Calculating balances')
			kraken_BTC_balance, kraken_balance = calculate_balances(kraken_client)

			time.sleep(1)

			logging.info('Calculating prices')
			high_bid_0_kraken, low_ask_0_kraken, high_bid_0_poloniex, low_ask_0_poloniex, high_bid_0_bittrex, low_ask_0_bittrex = get_prices_volumes(kraken_client)

			logging.info('Cancelling existing sell order and placing new sell order')
			PlaceLimitSellOrder(kraken_client, kraken_balance, low_ask_0_bittrex, low_ask_0_poloniex, low_ask_0_kraken).execute()

			logging.info("Timestamp: {} Kraken {} Balance: {} Kraken BTC Balance: {} Kraken price: {} Poloniex price: {} Bittrex price: {}"\
				.format(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), currency, \
				kraken_balance, kraken_BTC_balance, high_bid_0_kraken, high_bid_0_poloniex, high_bid_0_bittrex))

			time.sleep(10)
		except Exception as e:
			logging.info(e)
			time.sleep(10)

if __name__ == "__main__":
	main()