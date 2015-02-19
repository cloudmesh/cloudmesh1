JobStatus = ['running', 'pending', 'completed', 'failed']

class Queue(document):

    name = StringField()
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
    


class Job(Document):

    name = StringField()
    jobid = StringField()
    group = StringField()
    user = StringField()
    ssh_config = StringField()
    status = StringField()
    queue = ReferenceField(Queue)

    def update(self):
        """updates the information e.g. the status of the job"""
        pass

    def info(self):
        """lists the info of the job"""
        pass

    def status(self):
        """status of the job"""
        return 0

queue = Queue(host='india.futuregrid.org',
              name='batch',
              ssh_config='india')
queue.save()


job = Job(name='job1',
          group='group1',
          user='gvonlasz',
          queue=queue)

job.status()





