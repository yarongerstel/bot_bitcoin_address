from ExtractInfoBitcoin import *
from QrScanner import *
from TelegramGetFile import *
from flask import Flask, request, Response
import requests
import sys
import os


class TelContact:
    """Department responsible for communication with the Telegram client"""
    # argv[1] contain the api_key of the bot
    # NGROK is used to make the server public
    TELEGRAM_INIT_WEBHOOK_URL = 'https://api.telegram.org/bot{}\
        /setWebhook?url=https://4308-79-179-181-57.eu.ngrok.io'.format(sys.argv[1])

    app = Flask(__name__)

    @staticmethod
    @app.route('/', methods=["POST"])
    def handle_message():
        """A primary function that extracts information it receives understands
         what it contains and thus decides to which function to send the data"""
        print("got message")
        chat_id = request.get_json()['message']['chat']['id']
        message = request.get_json()['message']

        if 'photo' not in message and 'text' not in message:  # get file unsupported
            response = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                                    .format(sys.argv[1], chat_id, 'unsupported'))
            return Response("success")

        elif 'photo' in message:
            print("got photo")
            # The message contains several image qualities. Last on the list in better quality
            file_id = message['photo'][-1]['file_id']
            upload_file = TelUploadFile(sys.argv[1], file_id)
            img = upload_file.get_image()
            qr = QrDecoder(img)
            data = qr.decode()
            if "bitcoin" in data:
                bitcoin_addresses = [data.split(":")[1]]
            elif data == "Failed to read image":  # can not decode the QR image
                bitcoin_addresses = [data]
            else:  # Proper QR code but not of Bitcoin
                bitcoin_addresses = ["This is not a wallet code"]
            # delete the photo file
            os.remove(img)
        else:  # 'text' in message:
            print("got text")
            answer = message['text']
            bitcoin_addresses = answer.split("\n")
        # For each address in the list checks the balance and returns to the client.
        # If the address is incorrect, an error message is returned to the client
        for address in bitcoin_addresses:
            bit_info = BitAddressInfo(address)
            res = bit_info.get_balance()
            if address == "Failed to read image" or address == "This is not a wallet code":
                res = ""
            response = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                                    .format(sys.argv[1], chat_id, address + "\n\n" + res))
        return Response("success")
