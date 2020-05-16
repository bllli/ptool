import os
import time
from datetime import datetime, timedelta
from typing import Tuple, Optional, List

from seeder.models import Task, Media
from Config import app as celery_app
import subprocess

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


@celery_app.task()
def gen_medias(task_id):
    task = Task.objects.get(id=task_id)
    medias = task.media.all()
    for media_index, media in enumerate(medias):
        # print(media.path)
        def check_error(result):
            msg, error = result
            if error:
                media.status = Media.Status.failed
                media.save()
                raise error  # 在这一层抛出 让media表记录错误状态
            return msg
        if os.path.isfile(media.path):
            media_info = check_error(call_subprocess(f'mediainfo {media.path}'))
            media.media_info = media_info
            video_info = check_error(call_subprocess(f'ffprobe -hide_banner {media.path}'))
            import re
            pattern = re.compile(r'Duration: (.*?), start')
            groups = pattern.search(video_info)
            if groups:
                base = datetime.strptime('00:00:00.00', '%H:%M:%S.%f')
                dt = datetime.strptime(groups[1], '%H:%M:%S.%f') - base
                seconds = dt.total_seconds()
                # todo load from config
                if seconds < 600:
                    slice_count = 2
                else:
                    slice_count = 9  # 切9张图
                offset_seconds = 20
                if seconds < 20:
                    slice_count = 1
                    offset_seconds = 10
                delta_pre_shot = seconds // slice_count
                if delta_pre_shot < 10:  # 省的越界
                    offset_seconds = 0
                times = []
                for i in range(slice_count):
                    shut = base + timedelta(seconds=delta_pre_shot * i + offset_seconds)
                    times.append(shut.strftime('%H:%M:%S'))
                shot_paths = []
                for shot_index, t in enumerate(times):
                    shot_path = f'tmp/{task_id}-{media.id}-{shot_index}.jpg'
                    check_error(call_subprocess(
                        f'ffmpeg -ss {t} -i {media.path} -f image2 -frames:v 1 -y {shot_path}'
                    ))
                    shot_paths.append(shot_path)
                media.screenshot = shot_paths
                media.save()  # 这儿先存一下？ 好像也没必要 反正都会重新截图生成
                # 上传到图床
                urls = [upload_image(path) for path in shot_paths]
                media.screenshot_bbcode = '\n'.join(map(lambda x: f'[img]{x}[/img]', urls))
                # 删了吧 占地方
                check_error(call_subprocess(f'rm tmp/{task_id}-{media.id}-*.jpg'))
        else:
            media.status = Media.Status.not_exists
        media.save()
    pass
