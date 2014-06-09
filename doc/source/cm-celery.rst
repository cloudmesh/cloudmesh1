CloudMesh and Celery
====================

CloudMesh uses Celery for asynchronous tasks with RabbitMQ messaging system.With Celery Task Queue, the web requests to CloudMesh GUI can be completed without waiting its process. The requested process runs in the background and update the result through Celery worker and RabbitMQ broker program. This helps improve performance of a web user interface of CloudMesh and perform parallel executions in the background.

Directory Structure
--------------------
In CloudMesh, Celery apps ans tasks are in a separated directory in each application. Here is what the directory looks like:

- ./queue/tasks.py
- ./queue/celery.py

* tasks.py: Contains tasks of Celery Task Queue
* celery.py: Contains apps of Celery and its configurations


