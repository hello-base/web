web: newrelic-admin run-program python web.py
scheduler: python manage.py celery worker -B -E --maxtasksperchild=1000
worker: newrelic-admin run-program python manage.py celery worker -E --maxtasksperchild=1000
