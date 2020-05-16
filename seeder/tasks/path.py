from seeder.models import Task
from Config import app as celery_app


@celery_app.task()
def path_to_medias(task_id):
    task = Task.objects.get(id=task_id)
    paths = task.path.all()

    pass
