import time

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.template.response import SimpleTemplateResponse

from django.conf import settings
from Config import app as celery_app
from seeder.oss.smms import SMMSClient
from seeder.oss.thumbsnap import ThumbSnapClient
from seeder.tasks.media import gen_medias, call_subprocess
from seeder.tasks.path import path_to_medias
from seeder.tasks.task import generate_torrent_file


def index(request):
    # from django.conf import settings
    # print(settings.SMMS_TOKEN)
    # smms = SMMSClient()
    # smms.profile()
    # smms.upload('tmp/1-0-2.jpg')
    # c = ThumbSnapClient()
    # c.upload('tmp/1-0-2.jpg')
    # gen_medias(1)
    # generate_torrent_file(4)
    # path_to_medias.delay(1)
    # from seeder.client.haidan import HaiDanClient
    # c = HaiDanClient()
    # if c.check():
    #     print(c.upload(1))
    # print(2)
    return SimpleTemplateResponse('index.html')


def self_check(request):
    return JsonResponse({
        'oss': {
            'smms': {
                'token': settings.SMMS_TOKEN,
                'check': False,
                'msg': '上传失败!\n1\n2\n3\n4',
            },
            'thumb': {
                'token': settings.THUMBSNAP_TOKEN,
                'check': False,
                'msg': '无效!'
            }
        },
        'ffmpeg': call_subprocess('ffmpeg -version'),
        'mediainfo': call_subprocess('mediainfo --version'),
    })
