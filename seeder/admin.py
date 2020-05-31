from django.contrib import admin

from django.db import models
from django.forms import ClearableFileInput, PasswordInput, BaseInlineFormSet

from .models import FilePath, Task, Media
from seeder.tasks.path import path_to_medias


class InlineFormSet(BaseInlineFormSet):
    def save(self, commit=True):
        obj = super().save(commit)
        obj[0].task.on_update_path()
        return obj

    def save_existing(self, form, instance, commit=True):
        # raw_path = instance.path
        obj = super().save_existing(form, instance, commit)
        # new_path = obj.path
        # if raw_path != new_path:
        #     obj.mark_updated()
        return obj


class FilePathInline(admin.StackedInline):
    # fields = ['id']
    model = FilePath
    extra = 0
    readonly_fields = ('status',)

    # formset = InlineFormSet

# class WebSiteInline(admin.StackedInline):
#     model = WebSite
#     extra = 0
#     exclude = ('celery_task_id',)
#     readonly_fields = ('status',)


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

    # def save_related(self, request, form, formsets, change):
    #     return super().save_related(request, form, formsets, change)

    # def save_formset(self, request, form, formset, change):
    #     return super()

    def save_form(self, request, form, change):
        return super().save_form(request, form, change)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # obj.on_update_path()
        # celery_task = path_to_medias(self.id)
        # celery_task = path_to_medias.delay(obj.id)
        # print(celery_task)

