import requests


class BitAddressInfo:
    """ A class that receives a Bitcoin wallet address and extracts information from that address"""

    def __init__(self, bitcoin_address):
        self._bitcoin_address = bitcoin_address
        self._transactions_url = 'https://blockchain.info/multiaddr?active={}'.format(bitcoin_address)
        self._bit_info = requests.get(self._transactions_url).json()

    def hes_exist(self):
        """ A function that checks if the address exists"""
        if 'addresses' in self._bit_info:
            return True
        else:
            return False

    def get_balance(self):
        """ A function that returns the balance of the existing amount in the wallet address
            If the address does not exist returns an error message: "invalid address" """
        if self.hes_exist():
            final_balance = self._bit_info['addresses'][0]['final_balance'] / 10 ** 8
            return "final_balance: " + str(final_balance) + " BTC"
        else:
            return self._bit_info['message']
