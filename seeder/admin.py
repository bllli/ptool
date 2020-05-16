from django.contrib import admin

from django.db import models
from django.forms import ClearableFileInput, PasswordInput

from .models import FilePath, Task, WebSite, Media


class FilePathInline(admin.StackedInline):
    # fields = ['id']
    model = FilePath
    extra = 0


class WebSiteInline(admin.StackedInline):
    model = WebSite
    extra = 0
    exclude = ('celery_task_id',)
    readonly_fields = ('status',)


# class RichTextEditorWidget(object):
#     pass


class MediaInline(admin.StackedInline):
    model = Media
    extra = 0
    exclude = ('celery_task_id',)
    readonly_fields = ('status', 'media_info')
    formfield_overrides = {
        models.FilePathField: {'widget': ClearableFileInput},
    }


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    inlines = (FilePathInline, WebSiteInline, MediaInline)
    # fields = ['id']
    readonly_fields = ('status', )
    pass
