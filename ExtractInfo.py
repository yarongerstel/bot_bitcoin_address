import requests
import json


class BitAddressInfo:

    def __init__(self, bitcoin_address):
        self._bitcoin_address = bitcoin_address
        self._transactions_url = 'https://blockchain.info/multiaddr?active=' + bitcoin_address
        self._bit_info = requests.get(self._transactions_url).json()

    def hes_exist(self):
        if 'addresses' in self._bit_info:
            return True
        else:
            return False

    def get_balance(self):
        if self.hes_exist():
            final_balance = self._bit_info['addresses'][0]['final_balance'] / 10 ** 8
            return "final_balance: " + str(final_balance) + " BTC"
        else:
            return self._bit_info['message']


class TelUploadFile:

    def __init__(self, api_key, file_id):
        self._file_id = file_id
        self._api_key = api_key

    def get_image(self):
        try:
            url = f'https://api.telegram.org/bot{self._api_key}/getFile?file_id={self._file_id}'
            a = requests.post(url)
            json_resp = json.loads(a.content)
            file_pathh = json_resp['result']['file_path']
            url_1 = f'https://api.telegram.org/file/bot{self._api_key}/{file_pathh}'
            res = requests.get(url_1)
            file_content = res.content  # the image in bytes
            with open(file_pathh.split("/")[-1], "wb") as f:
                f.write(file_content)
            return file_pathh.split("/")[-1]
        except:
            return 'fale to find the image'
