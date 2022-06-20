from pyzbar import pyzbar
from PIL import Image


class QrDecoder:
    def __init__(self, image):
        self._image = image

    def decode(self):
        try:
            img = Image.open(self._image)
            qr_code = pyzbar.decode(img)[0]
            # convert into string
            data = qr_code.data.decode("utf-8")
            return data
        except:
            return "fail"
