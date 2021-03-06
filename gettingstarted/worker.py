from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gettingstarted.settings')
app = Celery('worker')
print('Celery: Start app')
# app = Celery('tasks', broker='redis://localhost:6379')
# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
print('Celery: Added app')
@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

