from django.apps import AppConfig
from django.db.models.signals import m2m_changed, post_save

from seeder.models import Task, FilePath


class SeederConfig(AppConfig):
    name = 'seeder'

    def ready(self):
        print('ready')
        from .signals import task_post_save, task_post_m2m_changed
        post_save.connect(task_post_save, sender=Task)
        m2m_changed.connect(task_post_m2m_changed, sender=FilePath.task)
