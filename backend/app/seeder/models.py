import os
from django.db import models
from django.db.models.signals import post_save, m2m_changed, pre_save
from jsonfield import JSONField
from filebrowser.fields import FileBrowseField

from Config import settings


class Task(models.Model):
    class Status(models.IntegerChoices):
        init = 1
        working = 2
        path_modified = 6
        failed = 8
        ok = 7
        published = 9

    class Type(models.IntegerChoices):
        Movies电影 = 401
        Documentaries动漫 = 404
        Animations动画 = 405
        TVSeries电视剧 = 402
        TVShows综艺 = 403
        MusicVideosMV = 406
        Sports体育 = 407
        Misc其他 = 409
        HQAudio音轨 = 408

    name = models.CharField('任务名称', max_length=255, default='新任务')
    status = models.IntegerField('任务状态', choices=Status.choices, default=Status.init)
    published = models.BooleanField('已发布', default=False)
    celery_task = models.CharField('celery task', max_length=36, blank=True, null=True)
    message = models.TextField('任务状态信息', default='', null=True, blank=True)
    pt_id = models.IntegerField('PT站生成的种子id', null=True, blank=True)
    # desc = models.TextField('最终生成的简介', null=True, blank=True)
    title = models.CharField('标题 要求规范填写，推荐英文', max_length=1000, null=False, blank=False)
    team_suffix = models.CharField('制作组后缀,必填', max_length=20, null=False, blank=False)
    sub_title = models.CharField('副标题', max_length=1000, null=True, blank=True)
    douban_url = models.URLField('豆瓣链接', null=True, blank=True)
    imdb_url = models.URLField('IMDB链接', null=True, blank=True)
    nfo = models.TextField('nfo信息', null=True, blank=True)
    image_urls = models.TextField('自动生成的图片', null=True, blank=True)
    other_bbcode = models.TextField('其他信息 格式为bbcode', null=True, blank=True)
    type = models.IntegerField('种子类型', choices=Type.choices, null=True, blank=False, default=401)
    season = models.IntegerField('第几季 0表示不区分季', null=True, blank=True)
    episode = models.CharField('第几集 0表示全集', null=False, blank=True, default='', max_length=100)
    collages = models.BooleanField('多季剧集/电影合集', null=True, default=False)

    medium = models.IntegerField('媒介', choices=[
        (1, 'Blu-ray'),
        (2, 'HD DVD'),
        (3, 'Remux'),
        (4, 'MiniBD'),
        (5, 'HDTV'),
        (6, 'DVDR'),
        (7, 'Encode'),
        (8, 'CD'),
        (9, 'UHD Blu-ray'),
        (10, 'SACD'),
        (11, 'WEB-DL'),
    ], null=True, blank=True, default=7)

    codec = models.IntegerField('编码', choices=[
        (1, 'H.264'),
        (2, 'VC-1'),
        (3, 'Xvid'),
        (4, 'MPEG-2'),
        (5, 'Other'),
        (11, 'H.265/HEVC/X265'),
        (13, 'MPEG-4/XviD/DivX'),
    ], null=True, blank=True, default=11)

    audiocodec = models.IntegerField('音频编码', choices=[
        (1, 'FLAC'),
        (2, 'APE'),
        (3, 'DTS'),
        (4, 'MP3'),
        (5, 'OGG'),
        (6, 'AAC'),
        (7, 'Other'),
    ], null=True, blank=True, default=3)

    standard = models.IntegerField('分辨率', choices=[
        (1, '4K/2160p'),
        (2, '2K/1080p'),
        (3, '1080i'),
        (4, '720p'),
        (5, 'SD')
    ], null=True, blank=True, default=2)

    def __str__(self):
        return f'<Task: {self.id} - {self.name}>'

    def get_path_status_text(self):
        return [FilePath.Status(path.status).name for path in self.path.all()]

    def get_media_status_text(self):
        return [Media.Status(media.status).name for media in self.media.all()]


class FilePath(models.Model):
    class Status(models.IntegerChoices):
        init = 1
        no_exists = 8
        ok = 9

    path = FileBrowseField("文件", max_length=200, directory="", blank=True)
    status = models.IntegerField('路径检测状态', choices=Status.choices, default=Status.init)

    task = models.ForeignKey(to=Task, to_field='id', related_name='path', on_delete=models.CASCADE)

    @staticmethod
    def check_status(**kwargs):
        # print('mark_updated:', self.id)
        # self.status = self.Status.init
        # self.save()
        print(1)

    def __str__(self):
        return f'{self.id}: {self.path}'


# pre_save.connect(FilePath.check_status, sender=FilePath)


class Media(models.Model):
    class Status(models.IntegerChoices):
        init = 1
        working = 5
        failed = 8
        ok = 9

    path = models.CharField('文件绝对路径', max_length=10000, blank=True, null=True)
    status = models.IntegerField('状态', choices=Status.choices, default=Status.init)
    message = models.TextField('状态信息', default='', blank=True, null=True)

    celery_task_id = models.IntegerField(blank=True, null=True)
    media_info = models.TextField('nfo', null=True, blank=True)

    using_oss = models.CharField('使用图床', max_length=100, default='THUMBSNAP')
    screenshot = JSONField('生成截图的绝对路径 [path, path]', blank=True, null=True)
    screenshot_task = models.CharField('celery task', max_length=36, blank=True, null=True)
    screenshot_bbcode = models.TextField(blank=True, null=True)

    task = models.ForeignKey(to=Task, to_field='id', related_name='media', on_delete=models.CASCADE)


# class WebSite(models.Model):
#     class Status(models.IntegerChoices):
#         init = 1
#         working = 5
#         generated = 9
#
#     url = models.URLField('链接')
#     celery_task_id = models.IntegerField(blank=True, null=True)
#     bbcode = models.TextField('生成结果', null=True, blank=True)
#     status = models.IntegerField('状态', choices=Status.choices, default=Status.init)
#
#     task = models.ForeignKey(to=Task, to_field='id', related_name='website', on_delete=models.CASCADE)


# from .signals import task_post_save

# pre_save.connect(task_post_save, sender=Task)
# pre_save.connect(path_pre_save, sender=FilePath)
