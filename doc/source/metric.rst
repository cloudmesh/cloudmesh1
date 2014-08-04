Cloudmesh Metric
======================================================================

.. toctree::
   :maxdepth: -1

::   

  cm-metric <cloud> -s <start>
                  -e <end> 
                  -u <user> 
                  --metric=<metric>
                  --period=<period> 
                  [-c <cluster>]


Routes
----------------------------------------------------------------------



::

  metric/cloud/<cloud>/<user>/<metric>/<start>/<end>/<period>


is equal to ::

  cm-metric <cloud> -s <start>
                  -e <end> 
                  -u <user> 
                  --metric=<metric>
                  --period=<period> 



::

  metric/cluster/<cluster>/<user>/<metric>/<start>/<end>/<period>

is equal to::

  cm-metric -s <start>
                  -e <end> 
                  -u <user> 
                  --metric=<metric>
                  --period=<period> 
                  -c <cluster>



??????

::

  metric/<cloud>/<cluster>/<user>/<metric>/<start>/<end>/<period>


  cm-metric <cloud> -s <start>
                  -e <end> 
                  -u <user> 
                  --metric=<metric>
                  --period=<period> 
                  -c <cluster>

