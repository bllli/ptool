from celery import shared_task

from seeder.client.haidan import HaiDanClient
from seeder.models import Task
from seeder.tasks.media import gen_medias
from seeder.tasks.path import path_to_medias
from seeder.tasks.task import generate_torrent_file
from Config import app as celery_app


@shared_task
def task_build(task_id):
    try:
        # 路径生成媒体对象
        path_to_medias(task_id)
        # 对每一个媒体对象 生成mediainfo / 截图
        gen_medias(task_id)
    except Exception as e:
        raise e


def stop_build_task(task_id):
    print('stop_build_task', task_id)
    task = Task.objects.get(id=task_id)
    medias = task.media.all()
    celery_app.control.revoke([task.celery_task] + [_.screenshot_task for _ in medias if _.screenshot_task])


@shared_task
def task_publish(task_id):
    try:
        # 生成种子文件
        generate_torrent_file(task_id)
        # 发布到海胆
        HaiDanClient().upload(task_id)
        pass
    except Exception as e:
        raise e

