import TelegramContact
import requests

if __name__ == '__main__':
    TelegramContact.TelContact.app.run(port=9004)
    requests.get(TelegramContact.TelContact.TELEGRAM_INIT_WEBHOOK_URL)
