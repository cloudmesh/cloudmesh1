from pprint import pprint
from cloudmesh import banner
from datetime import timedelta, datetime
from pytimeparse.timeparse import timeparse
from cloudmesh.management.cloudmeshobject import CloudmeshObject

from mongoengine import *
connect('cloudmesh', port=27777)

import numpy as np


def welford_variance(value, n=0.0, mean=0.0, M2=0.0):
    n += 1
    delta = value - mean
    mean = mean + delta / n
    M2 = M2 + delta * (value - mean)
    population_variance = M2 / n
    sample_variance = M2 / (n - 1)
    return population_variance, sample_variance, n, mean, M2


class Cache(CloudmeshObject):
    id = StringField(primary_key=True)
    value = DictField(required=True)
    cm_kind = "cache"
    start_time = StringField()
    end_time = StringField()
    stat = DictField()

    @staticmethod
    def update(key, f, value):
        id = key + f.__name__
        entry = Cache(id=id, value=value)
        print "KEYS", value.keys()
        entry.save()

    @staticmethod
    def get(key, f):
        id = key + f.__name__
        print "OOOOO", id
        try:
            entry = Cache.objects(id=id)[0]._data
        except:
            entry = None
        return entry

    @staticmethod
    def get_id(key, f):
        id = key + f.__name__
        return id


def time_expired(time, delta):
    time_valid = time + timedelta(seconds=delta)
    not_valid = datetime.now() > time_valid
    return not_valid


def Sequential(credential, f, delta=4, **kwargs):
    result = {}
    for host in credential:
        entry = Cache.get(host, f)
        time_stamp = entry["date_modified"]
        if entry is None or time_expired(time_stamp, delta):
            user = credential[host]
            print "submitting -> {0}@{1}".format(user, host)
            result[host] = f(host=host, username=user, **kwargs)
            Cache.update(host, f, result[host])
        else:
            result[host] = entry["value"]
    return result


def Parallel(credential, f, delta=4, **kwargs):
    task = {}
    result = {}
    update = []

    for host in credential:
        entry = Cache.get(host, f)
        time_stamp = entry["date_modified"]
        #time_valid = time_stamp + timedelta(seconds=delta)
        #exired = datetime.now() > time_valid

        if (entry is None) or (time_expired(time_stamp, delta)):
            user = credential[host]
            id = Cache.get_id(host, f)
            print "submitting -> {0}@{1}".format(user, host)
            update.append(host)
            task[host] = f.apply_async(args=(host, user),
                                       kwargs=kwargs,
                                       expires=10, task_id=id)
        else:
            result[host] = entry["value"]

    banner("tasks", c=".")
    pprint(task)
    print update

    for host in update:
        print "getting -> {0}".format(host), str(task[host])
        result[host] = task[host].get(propagate=False)
        banner("info")
        print "INFO", task[host].info
        banner("result")
        print "RESULT", task[host].result
        banner("backend")
        print "BACKEND", task[host].backend
        Cache.update(host, f, result[host])

    return result
