from __future__ import absolute_import

from celery import Celery

celery_rain_queue = Celery('cloudmesh.rain.cobbler.queue.celery',
                           broker='amqp://guest@localhost',
                           backend='amqp://guest@localhost',
                           include=['cloudmesh.rain.cobbler.queue.tasks'])

# Optional configuration, see the application user guide.
celery_rain_queue.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
    CELERY_DISABLE_RATE_LIMITS=True,
)

if __name__ == '__main__':
    celery_rain_queue.start()
