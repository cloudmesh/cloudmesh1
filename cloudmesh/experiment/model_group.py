#
# terminal 1: fab manage.mongo
# terminal 2: python model_group.py 
#

from mongoengine import *
from pprint import pprint
from cloudmesh_common.tables import  array_dict_table_printer
import json 

db =  connect ('experiments', port=27777)



class ExperimentBase(Document):
    label = StringField()
    userid = StringField()
    meta = {'allow_inheritance': True}

    
class ExperimentVM(ExperimentBase):
    cloud = StringField()
    vmid = StringField()
        
class ExperimentGroup(object):

    def __init__(self, userid, label):
        self.userid = userid
        self.label = label
        
    def add(self, vm):
        vm.label = self.label
        vm.userid = self.userid
        vm.save()

    def get(self, label=None):
        if label is None:
            label = self.label
        # ide was, but does not work, so we use solution by hardcoding
        # args = ExperimentVM._fields
        # vms = ExperimentVM.objects(userid=self.userid, label=self.label).only(*args)
        
        vms = ExperimentVM.objects(userid=self.userid, label=label).only('userid',
                                                                         'label', 
                                                                         'cloud',
                                                                         'vmid')
        return json.loads(vms.to_json())

    def delete(self,label):
        vms = ExperimentVM.objects(userid=self.userid, label=self.label)
        for vm in vms:
            vm.delete()        
        
    def to_table(self, label):
        data = self.get(label)
        if data == []:
            return "No data found"
        else:
            return array_dict_table_printer(data)
            

def main():

    username = "gregor"
    label = "exp-a"

    for i in range(1,10):
        vm = ExperimentVM(
            label = label,
            userid = username,
            cloud = "india_openstack_havana",
            vmid = "myid-{0}".format(i),
            )
        vm.save()

    
    vms = ExperimentVM.objects()
    for vm in vms:
        print vm.label, vm.userid, vm.vmid, vm.cloud

    experiment = ExperimentGroup(username, label)

    print experiment.to_table(label)

    
    experiment.delete(label)
    print experiment.to_table(label)    
    
    
if __name__ == "__main__":
    main()
