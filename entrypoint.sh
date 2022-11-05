#!/bin/sh
set -xeu

python vksearch/manage.py migrate
#python  vksearch/manage.py collectstatic --no-input --clear

exec "$@"
