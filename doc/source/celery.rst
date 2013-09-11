.. sidebar:: Page Contents

   .. contents::
      :local:


.. sectnum::
   :start: 3

   
**********************************************************************
Celery Setup
**********************************************************************
For running celery you will need the celery package. This is a python package for asynchronus message passing and queuing. If you dont already have it, you can get that by::

	$ pip install celery
	
You will also need RabbitMQ whihc is the celery broker we use. If you dont already have it you cna get it by::

	$ sudo apt-get install rabbitmq-server

More on the first steps to celery can be found in the `Celery Documentation <http://docs.celeryproject.org/en/latest/getting-started/first-steps-with-celery.html>`_
   

 Starting and Stopping Celery
======================================================================

The celery can be started by the following command

   $ fab queue.start
   
Currently the implementation supports two workers(queue) each for
provisioner (called p1,p2) and launcher (called l1,l2). This command will stop these workers if they are already running and kill celery.
This command needs you to sudo. 

The celery can be stopped by the following command which stops celery and kills all celery workers::

	$ fab server.stop
	
The celery can be cleaned by the following command kills all celery workers::

	$ fab server.clean


Log and Pid Files
======================================================================

These log files have the log information for the workers and pid files have the pid information. One log and pid file is created for each worker. All information written to the standard output in the celery tasks will be found the log file.
If the name of the worker is abc. Then we will have celery@abc.log and celery@abc.pid.
If there are more than one worker for any task, the task can be performed by any of the worker associated to it. The log will be in .log file which actually did the task. SO make sure you check .log files of all asoociated workers.


Current Celery Based Tasks
======================================================================

Launcher (Simulation)
----------------------------------------------------------------------
The launcher can be run from **/cm/launch**. You can select the server, and recipie and press the **press to launch** button. This will submit the jobs to celery.
These status of all of the jobs can be viewed at **/cm/launch/db_stats**. 
You can clean the stats at **/cm/db_reset**. 
