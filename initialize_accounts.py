import kraken.api as kraken
import poloniex.__init__ as poloniex
import bittrex.bittrex as bittrex
from support_functions import load_key, get_input_args

def initialize_accounts():
	#Kraken
    Vadim_Kraken = kraken.API()
    api_key_name = get_input_args().currency_pair
    if api_key_name == "RIPPLE":
        Vadim_Kraken.load_key(r"kraken/RIPPLE_KEY_FOLDER/key.txt")
    elif api_key_name == "ETC_CLASSIC":
        Vadim_Kraken.load_key(r"kraken/ETC_CLASSIC_KEY_FOLDER/key.txt")
    elif api_key_name == "ATOM":
        Vadim_Kraken.load_key(r"kraken/ATOM_KEY_FOLDER/key.txt")
    elif api_key_name == "MONERO":
        Vadim_Kraken.load_key(r"kraken/MONERO_KEY_FOLDER/key.txt")
    elif api_key_name == "DASH":
        Vadim_Kraken.load_key(r"kraken/DASH_KEY_FOLDER/key.txt")
    elif api_key_name == "STELLAR":
        Vadim_Kraken.load_key(r"kraken/STELLAR_KEY_FOLDER/key.txt")

    #Poloniex
    Vadim_Poloniex = poloniex.Poloniex()
    Vadim_Poloniex.load_key(r"poloniex/key.txt")
    #Bittrex
    api_key, api_secret = load_key(r"bittrex/key.txt")
    Vadim_Bittrex = bittrex.Bittrex(api_key = api_key, api_secret = api_secret)
    #return class instances
    return Vadim_Kraken, Vadim_Poloniex, Vadim_Bittrex
