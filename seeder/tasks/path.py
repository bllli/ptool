import os
import time

from celery import shared_task
from filetype import filetype

from seeder.models import Task, FilePath, Media
from Config import app as celery_app


# @celery_app.
@shared_task
def path_to_medias(task_id):
    time.sleep(3)
    print('path_to_medias', task_id)
    task = Task.objects.get(id=task_id)
    path_ms = task.path.all()
    medias_path = []

    def add_to_list(p) -> bool:
        kind = filetype.guess(p)
        if kind and kind.MIME.startswith('video/'):
            medias_path.append(p)
            return True
        return False
    for path_m in path_ms:
        status = FilePath.Status.no_exists
        full_path = path_m.path.path_full
        if os.path.isdir(full_path):
            for root, dirs, files in os.walk(full_path, topdown=False):
                for name in files:
                    print(os.path.join(root, name))
                    file_path = os.path.join(root, name)
                    if add_to_list(file_path):
                        status = FilePath.Status.ok
        elif os.path.isfile(full_path):
            if add_to_list(full_path):
                status = FilePath.Status.ok
        path_m.status = status
        path_m.save()
    print(medias_path)
    task.media.all().delete()
    for media_path in medias_path:
        task.media.create(path=media_path)

    if not medias_path:
        task.status = Task.Status.failed
        task.message = '路径中找不到视频文件'
        task.save()
    from seeder.tasks.media import gen_medias
    gen_medias.delay(task_id)
    pass
