#!/bin/sh
mkdir -p tmp
python3 manage.py migrate --noinput
python3 manage.py initadmin
python3 manage.py collectstatic
