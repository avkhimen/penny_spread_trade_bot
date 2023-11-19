import argparse
import datetime

def load_key(path):
	with open(path, 'r') as f:
		key = f.readline().strip()
		secret = f.readline().strip()
	return key, secret

def get_input_args():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('currency_pair', type = str, choices = ['RIPPLE', 'DASH', 'DOGE'], default = 'RIPPLE', 
	                    help = 'currency pair to trade')
    return parser.parse_args()

def get_timestamp_from_unix(timestamp):

	timestamp = datetime.datetime.fromtimestamp(timestamp)

	return timestamp.strftime('%Y-%m-%d %H:%M:%S')