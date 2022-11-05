#!/bin/sh
set -xeu

python manage.py migrate
python manage.py collectstatic --no-input --clear

exec "$@"
