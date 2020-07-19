import time
from pprint import pprint

import requests
from constance import config


def get_token():
    return config.SMMS_TOKEN


class SMMSClient:
    def __init__(self):
        self.token = get_token()
        self.base_url = 'https://sm.ms/api/v2/'

    def _post(self, url, data=None, files=None):
        return requests.post(
            self.base_url + url,
            data=data,
            files=files,
            headers={'Authorization': self.token}
        )

    def profile(self):
        resp = self._post('profile')
        data = resp.json()['data']
        if data['disk_limit_raw'] < (data['disk_usage_raw'] + 60000):
            raise EnvironmentError('你的SMMS账号空间不足')

    def upload(self, file_path):
        with open(file_path, 'rb') as f:
            start = time.time()
            resp = self._post('upload', files={'smfile': f.read()})
            data = resp.json()
            print('upload', file_path, 'spend:', time.time() - start)
            if data['code'] != 'success':
                if data['code'] == 'image_repeated':
                    return data['images']
                raise ConnectionError('图片上传失败!! json:' + str(resp.json()))
            pprint(data)
            return data['data']['url']
