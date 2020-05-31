from django.contrib import admin

from django.db import models
from django.forms import ClearableFileInput, PasswordInput, BaseInlineFormSet

from .models import FilePath, Task, Media


class FilePathInline(admin.StackedInline):
    # fields = ['id']
    model = FilePath
    extra = 0
    readonly_fields = ('status',)


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
    list_display = ('id', 'name', 'status', 'pt_url')
    inlines = (FilePathInline, MediaInline)
    # fields = ['id']
    readonly_fields = ('status', 'image_urls', 'pt_id')
    actions = ['retry', 'publish']

    def retry(self, request, queryset):
        return 1

    def publish(self, request, queryset):
        return 1

    def pt_url(self, model: Task):
        if model.status == Task.Status.published:
            return f'https://www.haidan.video/details.php?id={model.pt_id}'
        else:
            return ''

    def save_form(self, request, form, change):
        return super().save_form(request, form, change)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
