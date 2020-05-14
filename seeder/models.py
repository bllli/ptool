import os
from django.db import models
from jsonfield import JSONField

from Config import settings


class KV(models.Model):
    key = models.CharField(max_length=255, primary_key=True)
    value = models.TextField(default='')


class Task(models.Model):
    class Status(models.IntegerChoices):
        init = 1
        published = 9

    name = models.CharField('任务名称', max_length=255, default='新任务')
    status = models.IntegerField('任务状态', choices=Status.choices, default=Status.init)
    desc = models.TextField('最终生成的简介', null=True, blank=True)

    def __str__(self):
        return f'<Task: {self.id} - {self.name}>'


class FilePath(models.Model):
    # path = models.FilePathField(path=os.path.join(settings.BASE_DIR, 'tmp'), max_length=1000)
    path = models.FilePathField(path=os.path.join(settings.BASE_DIR, 'tmp'), max_length=1000)

    task = models.ForeignKey(to=Task, to_field='id', related_name='path', on_delete=models.CASCADE)

    def exists(self):
        return os.path.exists(self.path)

    def __str__(self):
        return f'做种文件/文件夹路径: {self.id} - 属于任务 {self.task_id}'


class Media(models.Model):
    class Status(models.IntegerChoices):
        init = 1
        working = 5
        generated = 9
    path = models.FilePathField(path=os.path.join(settings.BASE_DIR, 'tmp'), max_length=1000)
    status = models.IntegerField('', choices=Status.choices, default=Status.init)

    celery_task_id = models.IntegerField(blank=True, null=True)
    media_info = models.TextField('nfo', null=True, blank=True)

    screenshot = models.FilePathField(path=os.path.join(settings.BASE_DIR, 'tmp'), null=True, blank=True)
    screenshot_bbcode = models.TextField()

    task = models.ForeignKey(to=Task, to_field='id', related_name='media', on_delete=models.CASCADE)


class WebSite(models.Model):
    class Status(models.IntegerChoices):
        init = 1
        working = 5
        generated = 9
    url = models.URLField('链接')
    celery_task_id = models.IntegerField(blank=True, null=True)
    bbcode = models.TextField('生成结果', null=True, blank=True)
    status = models.IntegerField('状态', choices=Status.choices, default=Status.init)

    task = models.ForeignKey(to=Task, to_field='id', related_name='website', on_delete=models.CASCADE)
