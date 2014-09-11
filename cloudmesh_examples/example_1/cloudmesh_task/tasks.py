# from __future__ import absolute_import

from cloudmesh_task.celery import app
from sh import ssh
from pprint import pprint
import datetime


@app.task(track_started=True)
def cm_ssh(host, username=None, command=None):

    result = dict({
        "host": host,
        "command": command,
        "username": username,
        "output": None,
        "error": None,
        "time_start": None,
        "time_end": None
    })

    try:

        result["time_start"] = str(datetime.datetime.now())
        result["output"] = str(
            ssh("{0}@{1}".format(username, host), "date; " + command))
        # result["output"] = "DEBUG {0} {1}".format(host, str(now))
        result["time_end"] = str(datetime.datetime.now())

    except Exception, e:

        result["error"] = str(e)

    return result
