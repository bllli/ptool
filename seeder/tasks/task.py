from seeder.models import Task, Media
from Config import app as celery_app
from constance import config
from torf import Torrent
from seeder.tasks.path import path_to_medias


@celery_app.task()
def check_task(task_id):
    task = Task.objects.get(id=task_id)
    # media 汇总信息 -> task
    task_medias = task.media.all()
    if not task_medias:
        task.status = Task.Status.ok
        task.message = '路径中找不到视频文件,可以直接发布'
        task.save()
        return
    all_media_ok = all(map(lambda x: x.status == Media.Status.ok, task_medias))
    if not all_media_ok:
        task.status = Task.Status.failed
        task.message = '有视频没处理好'
        task.save()
        return
    generate_torrent_file(task_id)
    task.status = Task.Status.ok
    task.message = '处理完成'
    task.image_urls = '\n'.join([_.screenshot_bbcode for _ in task_medias])
    task.nfo = task_medias[0].media_info
    task.save()


def generate_torrent_file(task_id):
    task = Task.objects.get(id=task_id)

    text = 'PT发种🐔 by Github @bllli'
    t = Torrent(trackers=[config.Tracker],
                comment=text)
    t.private = True
    t.created_by = text
    file_paths = []
    for path_m in task.path.all():
        file_paths.append(path_m.path.path)
    t.filepaths = file_paths
    # t.name = task.title
    t.generate()
    t.write(f'tmp/{task_id}-{task.title}.torrent', overwrite=True)
    return
