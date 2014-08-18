Interactive Queues
----------------------------------------------------------------------

The current queing system contains the ability to run interactive
queues. This is quite usefule, if you need to debug programs
interactively that you will run than in a bacth queue. To use this
feature we provide here a simple exaple on how to use a node on bravo.


Start an interactive shell with X11 forwarding on bravo you have to
first login into india as the bravo queues are currently controlled on
india::

   ssh -Y india

Than you need to start an interactive node::

   qsub -I -q bravo -X

As xterm is currently not installed on bravo, you can test the X11
forwarding with::

   firefox




