from __future__ import absolute_import

from celery import Celery

celery_pbs_queue = Celery('cloudmesh.pbs.celery',
                          broker='amqp://guest@localhost',
                          backend='amqp://guest@localhost',
                          include=['cloudmesh.pbs.tasks'])

# Optional configuration, see the application user guide.
celery_pbs_queue.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
    CELERY_DISABLE_RATE_LIMITS=True
)

if __name__ == '__main__':
    celery_pbs_queue.start()
