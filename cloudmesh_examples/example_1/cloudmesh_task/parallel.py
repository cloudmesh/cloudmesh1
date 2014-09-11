from pprint import pprint
from cloudmesh import banner
from datetime import timedelta, datetime


def Sequential(execution_array, f, **kwargs):
    print "ARGS", kwargs
    result = {}
    for element in execution_array:
        print "submitting -> {0}".format(element)
        result[element] = f(element, **kwargs)
    return result


def Parallel(execution_array, f, **kwargs):
    task = {}
    for element in execution_array:
        print "submitting -> {0}".format(element)
        task[element] = f.apply_async(args=(element,),
                                      kwargs=kwargs,
                                      expires=10)

    banner("tasks", c=".")
    pprint(task)
    result = {}

    for element in execution_array:
        print "getting -> {0}".format(element), str(task[element])
        result[element] = task[element].get(propagate=False, no_ack=False)
        banner("info")
        print "INFO", task[element].info
        banner("result")
        print "RESULT", task[element].result
        banner("backend")
        print "BACKEND", task[element].backend

        # print "OOOO", result[element]

    return result
