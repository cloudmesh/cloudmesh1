HPC
=======================================

Cloudmesh provides a simple interface to view High Perfomance Computer clusters batch 
queues. This includes a python API, iPython examples,  a hosted user interface and a 
stand alone user interface. Currently we support Torques qstat and quinfo


:qinfo: Information about which queues are available

:qstat: Information which jobs ar ecurrently running

**Bugs**

Note that an older version of Torque is installed on FutureGrid, and sometimes 
returns negative numbers. In future we will upgrade this version to remove this bug.
Therefor some of the status information may not yet been accurate.
