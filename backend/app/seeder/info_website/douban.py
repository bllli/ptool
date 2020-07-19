from pprint import pprint

import requests


class DoubanDecodeClient:
    def __init__(self):
        pass

    def _get_from(self, url):
        resp = requests.get(
            f'https://api.rhilip.info/tool/movieinfo/gen?url={url}',
            headers={
                'authority': 'api.rhilip.info',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',

            }
        )
        pprint(resp.json())


if __name__ == '__main__':
    c = DoubanDecodeClient()
    c._get_from('https://movie.douban.com/subject/30402296')
