from celery import shared_task
from celery.signals import task_postrun


@shared_task
def divide(x, y):
    import time
    time.sleep(5)
    return x / y

@shared_task()
def sample_task(email):
    from project.users.views import api_call

    api_call(email)

@task_postrun.connect
def task_postrun_handler(task_id, **kwargs):
    from project.users.events import update_celery_task_status
    update_celery_task_status(task_id)