import time
from celery.decorators import task
from celery.utils.log import get_task_logger
# from gettingstarted.worker import app as celery_app
from listener.utils.worker import start_listening

logger = get_task_logger(__name__)
# @celery_app.task
@task(name="send_feedback_email_task")
def add_tweet(a):
    print(a)
    start_listening(['#macron'])

