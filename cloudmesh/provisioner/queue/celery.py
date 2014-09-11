from __future__ import absolute_import

from celery import Celery

celery_provisiner_queue = Celery('cloudmesh.provisioner.queue.celery',
                                 broker='amqp://guest@localhost',
                                 backend='amqp://guest@localhost',
                                 include=['cloudmesh.provisioner.queue.tasks'])

# Optional configuration, see the application user guide.
celery_provisiner_queue.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
    CELERY_DISABLE_RATE_LIMITS=True
)

if __name__ == '__main__':
    celery_provisiner_queue.start()
