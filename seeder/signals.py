from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from .tasks.path import path_to_medias
from .models import Task


# @receiver(post_save, sender=Task)
def task_post_save(sender, instance=None, created=False, **kwargs):
    celery_task = path_to_medias.delay(instance.id)
    print(celery_task)
    print('task_post_save', instance.id)


# @receiver(m2m_changed, sender=Task)
def task_post_m2m_changed(action, instance, reverse, model, pk_set, using, **kwargs):
    # celery_task = path_to_medias.delay(instance.id)
    # print(celery_task)
    print('task_post_m2m_changed', instance.id)
