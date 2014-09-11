from __future__ import absolute_import

from celery import Celery

app = Celery('cloudmesh_task',
             broker='amqp://guest@localhost//',
             backend='amqp://guest@localhost//',
             include=['cloudmesh_task.tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    CELERY_RESULT_BACKEND='amqp',
    CELERY_TASK_RESULT_EXPIRES=10,
    CELERY_ACCEPT_CONTENT=['json'],
    #    CELERY_ACCEPT_CONTENT = ['application/json'],
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='json',
    CELERY_DISABLE_RATE_LIMITS=True,
    CELERY_IGNORE_RESULT=False,
    CELERY_RESULT_EXCHANGE="qstatresults",
    CELERY_RESULT_PERSISTENT=False,
    CELERY_ENABLE_UTC=True,
    CELERY_TIMEZONE='US/Eastern',
    CELERY_MAX_CACHED_RESULTS=5,
    BROKER_POOL_LIMIT=0,
)


if __name__ == '__main__':
    app.start()
