from django.contrib import admin

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


class MediaInline(admin.StackedInline):
    model = Media
    extra = 0
    exclude = ('celery_task_id',)
    readonly_fields = ('status', 'media_info')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    inlines = (FilePathInline, WebSiteInline, MediaInline)
    # fields = ['id']
    readonly_fields = ('status', )
    pass
