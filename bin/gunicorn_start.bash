#!/bin/bash
NAME="findRice" # Name of the application
DJANGODIR=/home/findRice/findRice # Django project directory
SOCKFILE=/home/findRice/run/gunicorn.sock # we will communicte using this unix socket
USER=find_rice_runner # the user to run as
NUM_WORKERS=3 # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=findRice.settings # which settings file should Django use
DJANGO_WSGI_MODULE=findRice.wsgi # WSGI module name
 
echo "Starting $NAME as `whoami`"
 
# Activate the virtual environment
cd $DJANGODIR
source ../ENV/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH
# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR
# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
echo "Starting django service"
exec gunicorn ${DJANGO_WSGI_MODULE}:application \
--name $NAME \
--workers $NUM_WORKERS \
--user=$USER \
--bind=unix:$SOCKFILE \
--log-level=debug \
--log-file=-

echo "Starting celery service"
celery -A findRice worker --without-mingle
