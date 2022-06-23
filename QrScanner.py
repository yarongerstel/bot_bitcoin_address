from pyzbar import pyzbar
from PIL import Image


class QrDecoder:
    """A class that receives an image that contains a QR barcode and returns a decoding of the barcode"""

    def __init__(self, image):
        self._image = image

    def decode(self):
        """A function that receives an image that contains a QR barcode and returns decoding of the barcode"""
        try:
            img = Image.open(self._image)
            qr_code = pyzbar.decode(img)[0]  # Receives an object that contains information about the decryption
            data = qr_code.data.decode("utf-8")  # Extracts information about decode data from decode object
            return data
        except:
            return "fail reading image"
