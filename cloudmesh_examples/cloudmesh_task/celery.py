from __future__ import absolute_import

from celery import Celery

app = Celery('cloudmesh_task',
             broker='amqp://',
             backend='amqp://',
             include=['cloudmesh_task.tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    CELERY_RESULT_BACKEND = 'amqp',
    CELERY_TASK_RESULT_EXPIRES=5,     
    CELERY_ACCEPT_CONTENT = ['json'],
    #    CELERY_ACCEPT_CONTENT = ['application/json'],
    CELERY_TASK_SERIALIZER = 'json',
    CELERY_RESULT_SERIALIZER = 'json',    
    )



if __name__ == '__main__':
    app.start()
