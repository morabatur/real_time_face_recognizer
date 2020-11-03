import json

import requests


class ServerApi(object):
    def __init__(self, host):
        self.host = host

    def get(self, url: str):
        response = requests.get(self.host + url)
        json_data = json.loads(response.text)
        return json_data


    def rtsp_start(self, camera_id):
        url = self.host + '/rtsp/start/' + str(camera_id)
        response = requests.get(url)
        return response

    def rtsp_finish(self, camera_id):
        url = self.host + '/rtsp/finish/' + str(camera_id)
        response = requests.get(url)
        return response