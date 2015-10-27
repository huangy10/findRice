#!/bin/bash
DJANGO_DIR=/home/findRice/findRice
NAME="find_rice_celery"

echo "Starting $NAME"

cd $DJANGO_DIR
source ../ENV/bin/activate

celery worker -A findRice --loglevel=INFO --without-mingle
