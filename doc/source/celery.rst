.. sidebar:: Page Contents

   .. contents::
      :local:


.. sectnum::
   :start: 5

   
**********************************************************************
Celery Setup
**********************************************************************
For running celery you will need the celery package. This is a python package for asynchronus message passing and queuing. If you dont already have it, you can get that by::

	$ pip install celery
	
You will also need RabbitMQ whihc is the celery broker we use. If you dont already have it you cna get it by::

	$ sudo apt-get install rabbitmq-server

To find out more information about celery you can visit the `Celery Documentation <http://docs.celeryproject.org/en/latest/getting-started/first-steps-with-celery.html>`_
   

Starting and Stopping Celery
======================================================================

Within cloudmesh the use of celery is very simple as we have
introduced a number of easy to use commands. Celery server can be started by the following command::

   $ fab queue.start
   
For our test implementation we just start two workers each for the
queues

* provisioner (called p1,p2) 
* launcher (called l1,l2). 

Celery workers can be stopped by the following command which stops celery and kills all celery workers::

	$ fab queue.stop

Celery can be cleaned by the following command kills all celery
workers. It also deletesthe log files::

	$ fab queue.clean

Please note that the way we deployed celery it uses rabitmq which is
installed via sudo. Thus the commands will ask you for the sudo
password to controll the workers.




Log and Pid Files
======================================================================

Celery produces log files for the workers and pid files containing the
the pid information for the processes running. One log and pid file is
created for each worker. All information written to the standard
output in the celery tasks will be found the log file.  If the name of
the worker is abc, we will have celery@abc.log and celery@abc.pid.  If
there are more than one worker for any task, the task can be performed
by any of the worker associated to it. The log will be in .log file
which actually did the task.  Make sure you check .log files of all
asoociated workers in case of issues


Current Celery Based Tasks
======================================================================

Launcher (Simulation)
----------------------------------------------------------------------
The launcher can be run from the web browser with::

* http://127.0.0.1:5000/cm/launch

You can select the server, and recipie and press the

.. raw:: html

   <span class="label label-default">press to launch</span>


button. This will submit the jobs to celery.
The status of all of the jobs can be viewed at 

* http://127.0.0.1:5000/cm/launch/db_stats
 
You can clean the stats at 

* http://127.0.0.1:5000/cm/launch/db_stats/cm/db_reset**. 
