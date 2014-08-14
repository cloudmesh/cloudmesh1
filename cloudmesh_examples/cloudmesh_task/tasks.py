# from __future__ import absolute_import

from cloudmesh_task.celery import app
from sh import ssh 
from pprint import pprint
import datetime

@app.task
def cm_ssh(host, username=None, command=None):

    result = dict({
        "host": host,
        "command": command,
        "username": username, 
        "output": "None",
        "error": "None",
        "time": "None"
        })

    now = datetime.datetime.now()
    try:
        
        result["time"] = str(now)
        result["output"] = str(ssh("{0}@{1}".format(username, host), "date; " + command))
        # result["output"] = "DEBUG {0} {1}".format(host, str(now))

    except Exception, e:

        result["error"] = str(e)

    return result

    
