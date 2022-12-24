from celery import shared_task
from celery.signals import task_postrun


@shared_task
def divide(x, y):
    import time
    time.sleep(5)
    return x / y

@task_postrun.connect
def task_postrun_handler(task_id, **kwargs):
    from project.users.events import update_celery_task_status
    update_celery_task_status(task_id)