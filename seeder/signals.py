from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from .tasks.path import path_to_medias


def task_post_save(sender, instance=None, created=False, **kwargs):
    print('task_post_save', instance.id)
    from .models import Task, FilePath
    if not all(map(lambda x: x.status == FilePath.Status.ok, instance.path.all())) or\
            instance.status == Task.Status.path_modified:
        # celery_task = path_to_medias.delay(instance.id)
        # print('need update', celery_task)
        print(1)
    else:
        print('dont need update')
