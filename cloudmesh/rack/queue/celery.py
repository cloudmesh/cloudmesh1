from __future__ import absolute_import

from celery import Celery

celery_rack_queue = Celery('cloudmesh.rack.queue.celery',
                    broker='amqp://guest@localhost',
                    backend='amqp://guest@localhost',
                    include=['cloudmesh.rack.queue.tasks'])

# Optional configuration, see the application user guide.
celery_rack_queue.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
    CELERY_DISABLE_RATE_LIMITS=True,
    )

if __name__ == '__main__':
    celery_rack_queue.start()
