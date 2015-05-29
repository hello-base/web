web: gunicorn base.wsgi --log-file -
worker: celery worker -B -A base -E --maxtasksperchild=1000
