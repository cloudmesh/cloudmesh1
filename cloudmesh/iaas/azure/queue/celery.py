from __future__ import absolute_import
from celery import Celery

# Celery app for azure cloud
celery_azure_queue = Celery('cloudmesh.iaas.azure.queue',
                            broker='amqp://guest@localhost',
                            # mongodb://guest:guest@localhost:27017/jobs')#,
                            backend='amqp',
                            include=['cloudmesh.iaas.azure.queue.tasks'])

# Optional configuration, see the application user guide.
celery_azure_queue.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
    CELERY_DISABLE_RATE_LIMITS=True,
    CELERY_IGNORE_RESULT=False,
    CELERY_RESULT_PERSISTENT=True,
    CELERY_ENABLE_UTC=True,
    CELERY_TIMEZONE='US/Eastern'
)

if __name__ == '__main__':
    celery_azure_queue.start()
