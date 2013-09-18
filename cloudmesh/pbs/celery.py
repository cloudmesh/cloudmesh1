from __future__ import absolute_import

from celery import Celery

celery = Celery('cloudmesh.pbs.celery',
                broker='amqp://guest@localhost',
                backend='amqp://guest@localhost',
                include=['cloudmesh.pbs.tasks'])

# Optional configuration, see the application user guide.
celery.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
    CELERY_DISABLE_RATE_LIMITS=True
    )

if __name__ == '__main__':
    celery.start()

