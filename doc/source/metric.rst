METRIC
======

Metric command: 

  TBD


Routes
----------------------------------------------------------------------



::

  metric/cloud/<cloud>/<user>/<metric>/<start>/<end>/<period>


is eqal to ::

  cm-metric <cloud> -s <start>
                  -e <end> 
                  -u <user> 
                  --metric=<metric>
                  --period=<period> 



::
  metric/cluster/<cluster>/<user>/<metric>/<start>/<end>/<period>


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

