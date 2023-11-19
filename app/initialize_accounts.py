import kraken.api as kraken
from support_functions import load_key, get_input_args
import os

def initialize_accounts():

    kraken_client = kraken.API()

    with open('keys.txt', 'a') as file:
        l1 = str(os.environ['public_key']) + "\n"
        l2 = str(os.environ['private_key']) + "\n"
        file.writelines([l1, l2])
        file.close()
        
    kraken_client.load_key("keys.txt")

    os.remove("keys.txt")

    return kraken_client
