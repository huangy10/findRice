#!/bin/bash
DJANGO_DIR=/home/findRice/findRice
NAME="find_rice_celery"

echo "Starting $NAME"
echo $HOME

cd $DJANGO_DIR
source ~/.bash_profile
workon find_rice_env

celery worker -A findRice --loglevel=INFO --without-mingle
