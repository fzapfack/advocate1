web: gunicorn gettingstarted.wsgi --log-file -
worker: celery worker --app=gettingstarted.worker.app
# worker: python worker2.py