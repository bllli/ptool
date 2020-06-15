"""海胆PT站Client"""
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
        c = config.PT_COOKIES
        try:
            self.cookies = {_[0]: _[1] for _ in [_.strip().split('=') for _ in c.split(';')]}
        except Exception as e:
            raise Exception('cookies 格式有问题')

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
        }
        try:
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
                task_m.pt_id = int(params['id'])
            else:
                bs = bs4.BeautifulSoup(resp.content)
                ps = bs.find_all('p')
                ps = [p.text.strip() for p in ps if '魔力值' not in p.text and '打卡' not in p.text]
                task_m.message = '发布失败' + ';'.join(map(str, ps))
        except ConnectionError as e:
            task_m.message = '发布失败' + str(e)
        except Exception as e:
            task_m.message = '发布失败' + str(e)
        task_m.save()

    def upload_demo(self):
        params = {
            "file": ('1111.torrent', open('../../tmp/1111.torrent', 'rb').read()),
            "name": (None, '标题'),
            "small_descr": (None, '副标题'),
            "durl": (None, 'https://movie.douban.com/subject/33442331/'),
            "url": (None, 'http://www.imdb.com/title/tt12026744'),
            "preview-pics": (None, """https://thumbsnap.com/i/xefGa4oN.jpg
https://thumbsnap.com/i/sdCVBYzg.jpg
https://thumbsnap.com/i/PpCsWTMr.jpg
https://thumbsnap.com/i/PRGCUBjJ.jpg"""),
            "nfo-string": (None, """Unique ID : 182701576509801358962588017462883533822"""),
            "descr": (None, "其他描述"),
            "type": (None, 401),
            "medium_sel": (None, 1),
            "codec_sel": (None, 1),
            "audiocodec_sel": (None, 1),
            "standard_sel": (None, 1),
        }
        resp = requests.post(
            url=self.upload_url,
            cookies=self.cookies,
            files=params
        )
        print(1)


if __name__ == '__main__':
    c = HaiDanClient()
    # if c.check():
    print(c.upload_demo())
