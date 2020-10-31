import json

import requests


class ServerApi(object):
    def __init__(self, host):
        self.host = host

    def get(self, url: str):
        response = requests.get(self.host + url)
        json_data = json.loads(response.text)
        return json_data
