from __future__ import print_function
from mongoengine import *
from cloudmesh.config.cm_config import get_mongo_db, get_mongo_dbname_from_collection, DBConnFactory
from cloudmesh_base.logger import LOGGER
from pprint import pprint
import json
from cloudmesh.pbs.pbs import PBS
from cloudmesh import banner

log = LOGGER(__file__)

State = ['running', 'pending', 'completed', 'failed']


class QSub(Document):

    name = StringField()        
        
    dbname = get_mongo_dbname_from_collection("qsub")
    if dbname:
        meta = {'allow_inheritance': True, 'db_alias': dbname}
        
    @classmethod
    def remove(cls, name):
        element = cls.find(name)
        element.delete()

    @classmethod
    def find(cls, name):
        try:
            return cls.objects(name=name)[0]
        except:
            None

    @classmethod
    def reset(cls):
        for element in cls.objects:
            element.delete()

    @classmethod
    def connect(cls):
        get_mongo_db("qsub", DBConnFactory.TYPE_MONGOENGINE)
            
    
class Queue(QSub):

    host = StringField()
    user = StringField()
    """name in ssh/config"""

    def list():
        """lists the jobs in the queue"""
        pass

    def info(self, name=None):
        """lists the info of the queue if the name is None. 
        If name is other than none the specific queue info is given
        If the name is "all" info from all ques are returned."""
        pass        


class Job(QSub):

    name = StringField()
    jobid = StringField()
    group = StringField()
    user = StringField()
    ssh_config = StringField()
    state = StringField()
    queue = ReferenceField(Queue)

    @classmethod
    def list(cls):
        jobs = {}
        for job in cls.objects:
            jobs[job.name] = {'name': job.name,
                              'jobid': job.jobid,
                              'group': job.group,
                              'user': job.user,
                              'ssh_config': job.ssh_config,
                              'state': job.state}
        print("======")
        print(jobs)
        print("======")      
        
    @classmethod            
    def info(cls, name):
        """lists the info of the job"""
        job = cls.find(name)
        attributes = ["name", "jobid", "group", "user", "ssh_config", "state"]
        for attribute in attributes:
            try:
                print("{0:<10}: {1}".format(attribute, job[attribute]))
            except:
                print("{0}: {1}".format(attribute, 'undefind'))                

    @classmethod
    def status(cls, name):
        """state of the job"""
        try:
            job = cls.find(name)[0]
            print(job.name)
            return job.state
        except:
            return 'undefined'
                    
    def update(self):
        """updates the information e.g. the state of the job"""
        pass
        
    def submit(self):
        pass
    
    def remove(self):
        pass

    @classmethod
    def rename(cls, name_from, name_to):
        """BUG: does not work"""
        try:
            job_from = Job.find(cls, name_from)
            print (job_form)
        except:
            print("Error: the job to rename does not exist:", name_from)
            return
        
        try:
            job_to = Job.find(cls, name_to)
            print("Error: the to rename to already exists:", name_to)
            return
        except:
            pass
        
        job_from.name = name_to
        job_from.save()


QSub.connect()

queue = Queue(host='india.futuregrid.org',
              name='batch',
              ssh_config='india')
queue.save()

Job.reset()
Job.list()


name = 'job1'

job = Job(name=name,
          jobid=None,
          group='group1',
          user='gvonlasz',
          state='defined',
          ssh_config='india',
          queue=queue)
job.save()

# print (Job.status(name))

# jobs = Job.objects()

Job.list()

Job.info(name)

j = Job.find(name)

j.name = 'a'
j.save()

Job.list()

# # BUG
# Job.rename(name, 'job2')
# Job.info('job2')

banner("PBS")
pbs = PBS("gvonlasz", "india.futuregrid.org")
#pprint (pbs.qinfo())
pprint(pbs.qstat())

