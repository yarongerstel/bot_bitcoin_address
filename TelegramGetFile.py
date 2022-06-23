import json
import requests


class TelUploadFile:
    """A class that receives a file from the telegram and saves it on the local computer"""

    def __init__(self, api_key, file_id):
        self._file_id = file_id
        self._api_key = api_key

    def get_image(self):
        """A function that saves an image sent from the telegram on the local computer"""
        try:
            url = 'https://api.telegram.org/bot{}/getFile?file_id={}'.format(self._api_key, self._file_id)
            a = requests.post(url)
            json_resp = json.loads(a.content)
            file_pathh = json_resp['result']['file_path']
            url_1 = 'https://api.telegram.org/file/bot{}/{}'.format(self._api_key, file_pathh)
            res = requests.get(url_1)
            file_content = res.content  # the image in bytes
            with open(file_pathh.split("/")[-1], "wb") as f:
                f.write(file_content)
            return file_pathh.split("/")[-1]
        except:
            return 'Failed to find image on server'
