Q:

are we starting celery with  --events



RabbitMQ
======================================================================

List queues::

   rabbitmqctl list_queues name consumers

Tasks in queues::

   rabbitmqctl list_queues name messages messages_ready messages_unacknowledged

Memory::

    rabbitmqctl list_queues name memory


Celery
======================================================================

simple status

  celery status
     ?

  celery inspect ping

     import celery
     celery.current_app.control.inspect().ping()

  celery inspect stats

     import celery
     celery.current_app.control.inspect().stats()

     list of queues ;-)

     celery.current_app.control.inspect().stats().keys()

indo about celery:

   celery report
   celery inspect registered
   celery inspect report
   




Find active workers::

   celery inspect active

Active queues::

   celery inspect active_queues


Configuration::

   celery inspect conf

lots of data here

Memory::

  celery inspect memdump



What is this for?
----------------------------------------------------------------------

clock::


   celery inspect clock



REST for celery (not sure if useful and secure)
==================================================

http://cyme.readthedocs.org/en/latest/introduction.html
