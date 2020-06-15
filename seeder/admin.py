from django.contrib import admin

from django.db import models
from django.forms import ClearableFileInput, PasswordInput, BaseInlineFormSet
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe

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
    list_display = ('id', 'name', 'title', 'status', 'published', 'pt_url', 'message')
    inlines = (FilePathInline, MediaInline)
    # fields = ['id']
    readonly_fields = ('status', 'image_urls', 'pt_id', 'message', 'nfo', 'published', 'celery_task')
    actions = ['build', 'publish']

    def pt_url(self, instance):
        # assuming get_full_address() returns a list of strings
        # for each line of the address and you want to separate each
        # line by a linebreak
        if instance.pt_id:
            url = f'https://www.haidan.video/details.php?id={instance.pt_id}&hit=1'
            return mark_safe(f'<a target="_blank" href={url}>{url}</a>')
        else:
            return mark_safe(f"<span>未发布</span>")

        # return format_html_join(
        #     mark_safe('<br>'),
        #     '{}',
        #     ((line,) for line in instance.get_full_address()),
        # ) or mark_safe("<span class='errors'>I can't determine this address.</span>")

    # short_description functions like a model field's verbose_name
    pt_url.short_description = "URL"

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
        for task in queryset:
            if not task.published:
                # main_tasks.task_publish(task.id)
                main_tasks.task_publish.delay(task.id)

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
