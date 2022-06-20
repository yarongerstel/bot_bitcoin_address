from ExtractInfo import *
from QrScanner import *
from flask import Flask, request, Response
import requests
import sys
import os


class TelContact:
    # argv[1] contain the api_key of the bot
    # NGROK is used to make the server public
    TELEGRAM_INIT_WEBHOOK_URL = 'https://api.telegram.org/bot{}/setWebhook?' \
                                'url=https://d06b-79-179-181-57.eu.ngrok.io'.format(sys.argv[1])
    app = Flask(__name__)

    @staticmethod
    @app.route('/', methods=["POST"])
    def handle_message():
        print("got message")
        try:  # try to get image message from client
            chat_id = request.get_json()['message']['chat']['id']
            # The message contains several image qualities. Last on the list in better quality
            file_id = request.get_json()['message']['photo'][-1]['file_id']
            upload_file = TelUploadFile(sys.argv[1], file_id)
            img = upload_file.get_image()
            qr = QrDecoder(img)
            data = qr.decode()

            if data == 'fail':  # can not decode the QR image
                bitcoin_addresses = [data]
            else:
                bitcoin_addresses = [data.split(":")[1]]
            # delete the photo file
            os.remove(img)
        except:  # get text message
            chat_id = request.get_json()['message']['chat']['id']
            answer = request.get_json()['message']['text']
            bitcoin_addresses = answer.split("\n")
        finally:
            for address in bitcoin_addresses:
                bit_info = BitAddressInfo(address)
                res = bit_info.get_balance()
                response = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                                       .format(sys.argv[1], chat_id, address + "\n\n" + res))
            return Response("success")


if __name__ == '__main__':
    TelContact.app.run(port=9004)
    requests.get(TelContact.TELEGRAM_INIT_WEBHOOK_URL)
