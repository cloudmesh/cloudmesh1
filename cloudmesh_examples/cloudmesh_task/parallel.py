from cloudmesh_common.util import banner
from pprint import pprint

def Sequential (execution_array, f, **kwargs):
    result = {}
    for element in execution_array:
        result[element] = f(element, **kwargs)
    return result
                
def Parallel (execution_array, f, **kwargs):
    task = {}
    banner("SUBMIT")
    for element in execution_array:
        task[element] = f.delay(element, **kwargs)

    pprint (task)
    
    banner("COLLECT")
    result = {}
    for element in execution_array:
        banner (element, c=".")      
        task[element].get(propagate=False)
    return result
