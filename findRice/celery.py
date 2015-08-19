# put this file in a single file named celery.py in your project
# folder

# imports absolute imports from the future, so that the celery.py
# won't clash with the library
from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings
# set the default Django settings module for the 'celery' program.
# so that the celery commnad line program will know where your Django
# project is.
# This statement will always appear before the app instance is created
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'findRice.settings')
# always follows with app instance
# although we could have many instances, but we usually don't do like that
app = Celery('testCelery', broker='amqp://',
             backend='amqp://')
app.conf.update(
    CELERY_TASK_EXPIRES=3600,
)
# Using a string here means the worker will not have to pickle the
# object when using windows
# add the django settings module as a configuration source for celery
# so we can put the celery settings in the same settings.py
app.config_from_object('django.conf:settings')

# Use this command so that we can define tasks.py in each django app
# Use lambda so that autodiscovery only occurs when neccessary
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# this is just a test task


@app.task(bind=True)
def debug_task(self):
    print('Request:{0!r}'.format(self.Request))


if __name__ == '__main__':
    app.start()
