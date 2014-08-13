from __future__ import absolute_import

from cloudmesh_task.celery import app
from sh import ssh 

@app.task
def cm_ssh(host, username, command):
    print "{0}@{1}:{2}".format(username, host, command)
    output = ""
    error = None
    try:
        output = ssh("{0}@{1}".format(username, host), command)
    except Exception, e:
        error = dict({"host": host,
                    "username": username,
                    "command": command,
                    "error": e})
        
    return dict({"output": str(output),
                 "error": error})

