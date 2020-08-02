"""海胆PT站Client"""
import traceback

import bs4 as bs4
import requests

from seeder.models import Task
from constance import config


class HaiDanClient:
    def __init__(self):
        self.base_url = 'https://haidan.video/'
        self.upload_url = 'https://haidan.video/takeupload.php'
        # self.url_user_details = 'userdetails.php'  # '?id={id}'
        self.header = {}
        self.cookies = None

    def _get(self, url, params):
        return requests.get(
            url, params=params,
            cookies=self.cookies
        )

    def check(self):
        resp = self._get(self.base_url, {})
        soup = bs4.BeautifulSoup(resp.content, features="html.parser")
        found = soup.find_all('a', text='个人信息')
        return bool(found)

    def upload(self, task_id):
        task_m = Task.objects.get(id=task_id)
        params = {
            "file": ('1.torrent', open(f'tmp/{task_id}-{task_m.title}.torrent', 'rb').read()),
            "name": (None, task_m.title),
            "small_descr": (None, task_m.sub_title),
            "durl": (None, task_m.douban_url),
            "url": (None, task_m.imdb_url),
            "preview-pics": (None, task_m.image_urls),
            "nfo-string": (None, task_m.nfo),
            "descr": (None, task_m.other_bbcode),
            "type": (None, task_m.type),
            "medium_sel": (None, task_m.medium),
            "codec_sel": (None, task_m.codec),
            "audiocodec_sel": (None, task_m.audiocodec),
            "standard_sel": (None, task_m.standard),
            "team_suffix": (None, task_m.team_suffix),
            "season": (None, task_m.season),
            "episode": (None, task_m.episode),
            "collages": (None, 1 if task_m.collages else 0),
        }
        try:
            c = config.PT_COOKIES
            try:
                self.cookies = {_[0]: _[1] for _ in [_.strip().split('=') for _ in c.split(';')]}
            except Exception as e:
                raise Exception('cookies 格式有问题')
            resp = requests.post(
                url=self.upload_url,
                cookies=self.cookies,
                files=params,
                timeout=30,
            )
            # 'https://test.haidan.video/details.php?id=21&uploaded=1'
            if '&uploaded=1' in resp.url:
                params = {s.split('=')[0]: s.split('=')[1] for s in resp.url.split('?')[-1].split('&')}
                task_m.published = True
                task_m.message = '发布成功'
                task_m.pt_id = int(params['torrent_id'])
            else:
                bs = bs4.BeautifulSoup(resp.content)
                ps = bs.find_all('p')
                ps = [p.text.strip() for p in ps if '魔力值' not in p.text and '打卡' not in p.text]
                task_m.message = '发布失败' + ';'.join(map(str, ps))
        except ConnectionError as e:
            task_m.message = '发布失败' + traceback.format_exc()
        except Exception as e:
            task_m.message = '发布失败' + traceback.format_exc()
        task_m.save()


if __name__ == '__main__':
    c = HaiDanClient()
