from django.apps import AppConfig
from django.db.models.signals import m2m_changed, post_save

from seeder.models import Task, FilePath


class SeederConfig(AppConfig):
    name = 'seeder'

    def ready(self):
        print('ready')
