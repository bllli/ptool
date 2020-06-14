#!/bin/sh
python /manage.py migrate --noinput && \
python /manage.py initadmin && \
celery -A Config worker -l info -E --logfile="tmp/celery_%n%I.log" -D && \
python /manage.py runserver 0.0.0.0:8000 >> tmp/log 2>&1
