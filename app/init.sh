#!/bin/sh
python /app/manage.py migrate --noinput && \
python /app/manage.py initadmin
