import os
import sys
from django.urls import include, path
from django.shortcuts import render
from django.core.wsgi import get_wsgi_application
from utils.status import check_info

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

if os.environ.get('env') == 'docker':
    APP_VERSION_FILE = '/app/VERSION'
    DEBUG = False
else:
    DEBUG = True
    APP_VERSION_FILE = '../app/VERSION'


def home(request):
    current_version = read_version(APP_VERSION_FILE)
    return render(request, 'hello.html', context=dict(
        title='发种🐔升级工具',
        current_version=current_version,
        check_info=check_info()
    ))


urlpatterns = [
    path('', home),
]

if DEBUG:
    from django.core.management import execute_from_command_line
    # execute_from_command_line(sys.argv)
    execute_from_command_line(['updater.py', 'runserver', '0.0.0.0:8001'])
else:
    import netius.servers
    application = get_wsgi_application()
    server = netius.servers.WSGIServer(app=application)
    server.serve(port=8001)
