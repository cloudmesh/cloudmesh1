"""
async task, get cluster temperature,
value of "-1" means cannot connect to server or get temperature
"""

from sh import ssh
from celery import Celery

celery = Celery('cloudmesh.rack.tasks', backend='amqp', broker='amqp://guest@localhost//')

@celery.task
def task_sensors(dict_idip):
    dict_data = {}
    for cluster in dict_idip.keys():
        print "fetch ... ", cluster
        dict_data[cluster] = {}
        for uid in dict_idip[cluster].keys():
            ip = cluster[uid]
            dict_data[cluster][uid]["ip"] = ip
            # fetch uid-ip server's temperature
            report = ssh("-o ConnectTimeout=1", "-o ConnectionAttempts=1", 
                         "user", ip, 
                         "sensors"
                         )
            temp = parseCpuTemperature(report)
            dict_data[cluster][uid]["temp"] = temp[0]
            
    # write current temperature data to mongo db
    # ....


# get the highest cpu temperature throught parseing the output of 'sensors'
    # return is a list including 2 elems, [36.0, C] or [36.0, F]
    # C or F is the unit name of temperature
    def parseCpuTemperature(self, values):
        lines = values.split("\n")
        cpu_lines = [x for x in lines if x.find("(high") > -1]
        tunit = "C"
        tmax = -1
        for line in cpu_lines:
            # position of degree sign
            pos_degree = line.find(u"\xb0")
            # position of + 
            pos_plus = line.find(u"+")
            tnum = float(line[pos_plus+1:pos_degree])
            tunit = line[pos_degree+1:pos_degree+2]
            if tnum > tmax:
                tmax = tnum
        
        return [tmax, tunit]
        
    