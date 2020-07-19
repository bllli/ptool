import os
import sys
import hashlib
import time

from django import forms
from django.http import JsonResponse
from django.urls import include, path
from django.shortcuts import render
from django.core.wsgi import get_wsgi_application
from utils.status import check_info, restart_app

from utils.version import read_version

os.environ.setdefault("DJANGO_SETTINGS_MODULE", __name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SECRET_KEY = '__secret_key__do__not__matter'
ALLOWED_HOSTS = ['*']

ROOT_URLCONF = __name__
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [os.path.join(BASE_DIR, 'templates')]
}]

# CORS_ORIGIN_ALLOW_ALL = True
# INSTALLED_APPS = [
#     'corsheaders',
# ]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

if os.environ.get('env') == 'docker':
    APP_VERSION_FILE = '/app/VERSION'
    DEBUG = False
else:
    DEBUG = True
    APP_VERSION_FILE = '../app/VERSION'


def app_version(request):
    current_version = read_version(APP_VERSION_FILE)
    return JsonResponse({'data': current_version})


def app_status(request):
    try:
        system_check_info = check_info()
        system_check_info_err = False
    except ConnectionRefusedError:
        system_check_info = None
        system_check_info_err = '无法连接到supervisord'
    return JsonResponse({'err': system_check_info_err, 'info': system_check_info})


class UploadFileForm(forms.Form):
    file = forms.FileField()


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


update_file_info = {
    'md5': '',
    'updating': False,
    'restarting': False,
}


def read_update_file_in_service():
    if not os.path.isfile('/tmp/ptools/update.zip'):
        return
    global update_file_info
    update_file_info['md5'] = ''
    hash_md5 = hashlib.md5()
    with open('/tmp/ptools/update.zip', 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
        update_file_info['md5'] = hash_md5.hexdigest()


def handle_uploaded_file(f):
    global update_file_info
    update_file_info['md5'] = ''
    hash_md5 = hashlib.md5()
    with open('/tmp/ptools/update.zip', 'wb') as destination:
        for chunk in iter(lambda: f.read(4096), b""):
            destination.write(chunk)
            hash_md5.update(chunk)
        update_file_info['md5'] = hash_md5.hexdigest()


def app_upload_update_file(request):
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
        if '.zip' not in form.files.get('file').name:
            return JsonResponse({'msg': '必须是zip文件'})
        handle_uploaded_file(request.FILES['file'])
    return JsonResponse({'msg': 'ok'})


def app_get_update_file_info(request):
    if not os.path.isfile('/tmp/ptools/update.zip'):
        return JsonResponse({'msg': '文件不存在，请重新上传'})
    return JsonResponse({'msg': 'ok', 'info': update_file_info})


def app_update_confirm(request):
    global update_file_info
    if update_file_info['updating']:
        return JsonResponse({'status': '正在更新 请稍后'})
    update_file_info['updating'] = True
    # 停服务 删除以前的文件 新文件覆盖 迁移脚本 启动服务
    return JsonResponse({'msg': 'ok'})


def app_restart(request):
    time.sleep(3)
    return JsonResponse({'status': 'ok'})
    process = request.GET.get('process')
    restart_app(process)
    return JsonResponse({'status': 'ok'})


urlpatterns = [
    # path('', home),
    path('manager/app/version', app_version),
    path('manager/app/status', app_status),
    path('manager/app/restart', app_restart),
    path('manager/update/upload', app_upload_update_file),
    path('manager/update/check', app_get_update_file_info),
    path('manager/update/confirm', app_update_confirm),
]

read_update_file_in_service()


if DEBUG:
    from django.core.management import execute_from_command_line

    # execute_from_command_line(sys.argv)
    execute_from_command_line(['main.py', 'runserver', '0.0.0.0:8001'])
else:
    import netius.servers

    application = get_wsgi_application()
    server = netius.servers.WSGIServer(app=application)
    server.serve(port=8001)
