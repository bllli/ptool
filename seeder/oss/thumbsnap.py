import json
import time
from pprint import pprint

import requests
from django.conf import settings


class ThumbSnapClient:
    def __init__(self):
        self.token = settings.THUMBSNAP_TOKEN
        self.base_url = 'https://thumbsnap.com/api/'

    def _post(self, url, files=None):
        return requests.post(
            self.base_url + url,
            files=files,
        )

    def upload(self, file_path):
        # print('ThumbSnapClient', file_path, self.token)
        with open(file_path, 'rb') as f:
            start = time.time()
            resp = self._post('upload', files={
                'media': (file_path, f.read()), 'key': (None, self.token)
            })
            # print(resp.content)
            try:
                data = resp.json()
            except Exception as e:
                raise Exception(resp.content)
            print('upload', file_path, 'spend:', time.time() - start)
            pprint(data)
            if not data['success']:
                raise Exception(json.dumps(data))
            return data['data']['media']
