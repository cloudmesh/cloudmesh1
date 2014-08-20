CloudMesh and Celery
====================

CloudMesh uses Celery for asynchronous tasks with RabbitMQ messaging system. With Celery Task Queue, the web requests to CloudMesh GUI can be completed without waiting its process. The requested process runs in the background and update the result through Celery worker and RabbitMQ broker program. This helps improve performance of a web user interface of CloudMesh and perform parallel executions in the background.

Directory Structure
--------------------
In CloudMesh, Celery apps ans tasks are in a separated directory in each application. Here is what the directory looks like:

- ./queue/tasks.py
- ./queue/celery.py

* tasks.py: Contains tasks of Celery Task Queue
* celery.py: Contains apps of Celery and its configurations

Implementation
---------------

To quickly respond the web request, Celery task queue is used in CloudMesh to execute a process in the background. For example, launching a new vm instance, or retriving 20,000+ images on Amazon cloud may take some time. With Celery asynchronous task queue/job queue, these kind of long-running processes can be executed in the background. In CloudMesh, a couple of steps is required to apply Celery task queue to a existing process.

Place a new function call to execute a process with a celery task queue

Web GUI
=======

  - cloudmesh/cloudmesh_web/template/
  - cloudmesh/cloudmesh_web/modules/

App & Tasks
===========

 - [process]/queue/celery.py: celery app
 - [process]/queue/tasks.py: celery tasks for the process

Call a task
============

Celery has a function and a macro to execute a process in the background

- apply_async(); recommended because queue='azure-servers', for example, can be specified as a parameter.
- delay()

Queue Configuration
====================

Add a new property in a configuration file

 - .cloudmesh/cloudmesh_celery.yaml
   For example, adding azure-servers:

      azure-servers:
      id: a
      app: cloudmesh.iaas.azure.queue
      count: 1
      queue: azure-servers
      concurrency: 1

Broker Restart
==============

Broker restart will add a newly updated queue as a worker.

$ fab queue.stop
$ fab queue.start

Broker (RabbitMQ)
-----------------
Celery provides many options to choose a different broker such as Redis, MongoDB, etc. RabbitMQ is widely used to manage multiple queues and to distribute tasks by AMQP protocol. For more information see here: http://celery.readthedocs.org/en/latest/getting-started/brokers/index.html

Backend (Storing results)
-------------------------
With the backend setting of celery, the results of a completed task is stored on a selected backend broker. MongoDB database can be used to keep the results even after a broker restart.

Log File
--------

Each queue records INFO level event messages in the following directory.

- cloudmesh/celery/[queue].log

PID File
--------

Each queue keeps process id in a seperated file.

- cloudmesh/celery/[queue].pid
