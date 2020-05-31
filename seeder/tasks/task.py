from seeder.models import Task, Media
from Config import app as celery_app
from seeder.tasks.path import path_to_medias


@celery_app.task()
def task_main(task_id):
    path_to_medias(task_id)
    # path -> media
    # madia -> nfo / 截图 / 截图上传
    # media 汇总信息 -> task
    # task 上传 PT站
