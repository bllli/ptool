import time

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template.response import SimpleTemplateResponse


from Config import app as celery_app
from seeder.oss.smms import SMMSClient
from seeder.tasks.media import gen_medias


def index(request):
    from django.conf import settings
    print(settings.SMMS_TOKEN)
    # smms = SMMSClient()
    # smms.profile()
    # smms.upload('tmp/1-0-2.jpg')
    gen_medias(1)
    print(2)
    return SimpleTemplateResponse('index.html')
