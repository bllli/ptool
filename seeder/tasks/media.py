import os
import time
from datetime import datetime, timedelta
from typing import Tuple, Optional, List

from seeder.models import Task, Media
from Config import app as celery_app
import subprocess

from seeder.oss.smms import SMMSClient
from seeder.oss.thumbsnap import ThumbSnapClient
from seeder.upload_image import upload_image


def call_subprocess(command: str) -> Tuple[str, Optional[Exception]]:
    try:
        sp = subprocess.Popen(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        out = sp.communicate()
        msg = '\n'.join(map(lambda x: x.decode('utf-8'), out))
        return msg, None
    except Exception as e:
        return '', e


def gen_medias(task_id):
    print('gen_medias', task_id)
    task = Task.objects.get(id=task_id)
    medias = task.media.all()
    if not medias:
        print('no medias')
        return
    for media_index, media in enumerate(medias):
        print(media.path)

        def check_error(result):
            msg, error = result
            if error:
                media.status = Media.Status.failed
                media.save()
                raise error  # 在这一层抛出 让media表记录错误状态
            return msg

        if os.path.isfile(media.path):
            media_info = check_error(call_subprocess(f'mediainfo "{media.path}"'))
            media.media_info = media_info
            video_info = check_error(call_subprocess(f'ffprobe -hide_banner "{media.path}"'))
            import re
            pattern = re.compile(r'Duration: (.*?), start')
            groups = pattern.search(video_info)
            if groups:
                base = datetime.strptime('00:00:00.00', '%H:%M:%S.%f')
                dt = datetime.strptime(groups[1], '%H:%M:%S.%f') - base
                seconds = dt.total_seconds()
                # todo load from config
                if seconds < 600:
                    shot_num = 2
                else:
                    shot_num = 4
                offset_seconds = 20
                if seconds < 20:
                    shot_num = 1
                    offset_seconds = 10
                time_delta_pre_shot = seconds // shot_num
                if time_delta_pre_shot < 10:  # 省的越界
                    offset_seconds = 0
                shot_time_text_list = []
                for i in range(shot_num):
                    shut = base + timedelta(seconds=time_delta_pre_shot * i + offset_seconds)
                    shot_time_text_list.append(shut.strftime('%H:%M:%S'))
                # 截图前清场
                check_error(call_subprocess(f'rm tmp/{task_id}-{media.id}-*.jpg'))
                # 开始截图了!
                shot_paths = []
                for shot_index, t in enumerate(shot_time_text_list):
                    shot_path = f'tmp/{task_id}-{media.id}-{shot_index}.jpg'
                    check_error(call_subprocess(
                        f'ffmpeg -ss {t} -i "{media.path}" -f image2 -frames:v 1 -y {shot_path}'
                    ))
                    shot_paths.append(shot_path)
                media.screenshot = shot_paths
                media.save()  # 这儿先存一下 截图上传是另一个task，需要从数据库拿到最新数据
                # 上传到图床
                screenshot_task = upload_media_screenshot.delay(media.id, media.using_oss)
                media.screenshot_task = screenshot_task.id
            else:
                media.status = Media.Status.failed
                media.message = 'video_info信息有误： ' + video_info
            media.save()
        else:
            media.status = Media.Status.failed
            media.save()
    pass


OSS_CLIENT = {
    'THUMBSNAP': ThumbSnapClient,
    'SMMS': SMMSClient
}


@celery_app.task()
def upload_media_screenshot(media_id, using='THUMBSNAP'):
    """异步上传"""
    media = Media.objects.get(id=media_id)
    try:
        client = OSS_CLIENT.get(using)
        c = client()
        # code = '\n'.join([f'[img]{c.upload(path)}[/img]' for path in media.screenshot])
        code = '\n'.join([f'{c.upload(path)}' for path in media.screenshot])
        media.screenshot_bbcode = code
        media.status = Media.Status.ok
        media.message = '图片上传中'
        media.save()
        from seeder.tasks.task import check_task
        check_task.delay(media.task_id)
    except Exception as e:
        media.status = Media.Status.failed
        media.message = '上传过程出错:' + str(e)
        media.save()
