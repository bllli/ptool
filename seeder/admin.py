from django.contrib import admin

from django.db import models
from django.forms import ClearableFileInput, PasswordInput, BaseInlineFormSet
from .tasks import main as main_tasks
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
    readonly_fields = ('status', 'media_info', 'screenshot')
    formfield_overrides = {
        models.FilePathField: {'widget': ClearableFileInput},
    }


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status', 'published', 'pt_url', 'message')
    inlines = (FilePathInline, MediaInline)
    # fields = ['id']
    readonly_fields = ('status', 'image_urls', 'pt_id', 'message', 'nfo', 'published')
    actions = ['build', 'publish']

    def build(self, request, queryset):
        """生成"""
        for task in queryset:
            if not task.published:
                main_tasks.stop_build_task(task.id)
                celery_task_id = main_tasks.task_build.delay(task_id=task.id)
                # celery_task_id = main_tasks.task_build(task_id=task.id)
                print(celery_task_id)
                task.celery_task = celery_task_id
                task.save()

    def publish(self, request, queryset):
        """发布"""
        return 1

    def pt_url(self, model: Task):
        if model.status == Task.Status.published:
            return f'https://www.haidan.video/details.php?id={model.pt_id}'
        else:
            return ''

    # def save_form(self, request, form, change):
    #     return super().save_form(request, form, change)
    #
    # def save_model(self, request, obj, form, change):
    #     super().save_model(request, obj, form, change)
    #     print('save model', obj.id)
    #
    # def save_related(self, request, form, formsets, change):
    #     super().save_related(request, form, formsets, change)
    #     print('save_related')
    #
    # def save_formset(self, request, form, formset, change):
    #     super().save_formset(request, form, formset, change)
