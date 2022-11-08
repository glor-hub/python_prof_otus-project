#!/bin/bash
set -xeu
#make --quiet --directory="$HOME/celery" clean-pyc

echo "Apply migrations"
#if [ "$DATABASE" = "postgres" ]
#then
#    echo "Waiting for postgres..."
#
#    while ! nc -z $SQL_HOST $SQL_PORT; do
#      sleep 0.1
#    done
#
#    echo "PostgreSQL started"
#fi


python ./manage.py migrate
python ./manage.py collectstatic --noinput

#python vksearch/manage.py migrate
#python manage.py collectstatic --no-input --clear

exec "$@"

#!/usr/bin/env bash

#set -e
#
#echo "Apply migrations"
#
#flask db upgrade
#
#echo "migrations ok"
#
#exec "$@"

# prestart.sh echo hello world

# Apply migrations
# upgrade..
# migrations ok
# hello world