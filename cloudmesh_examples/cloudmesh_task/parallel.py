from pprint import pprint
from cloudmesh_common.util import banner
from datetime import timedelta, datetime

def Sequential (execution_array, f, **kwargs):
    print "ARGS", kwargs
    result = {}
    for element in execution_array:
        result[element] = f(element, **kwargs)
    return result


                
def Parallel (execution_array, f, **kwargs):
    task = {}
    for element in execution_array:
        task[element] = f.apply_async(args=(element,),
                                      kwargs=kwargs,
                                      expires=1)

    banner ("tasks", c=".")
    pprint (task)
    result = {}

    for element in execution_array:
        
        banner ("{0} {1}".format(element, task[element]), c=".")      
        result[element] = task[element].get(propagate=False)
        print "OOOO", result[element]

    return result
