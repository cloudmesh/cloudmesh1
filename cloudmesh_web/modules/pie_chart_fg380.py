from cloudmesh.config.cm_config import cm_config, cm_config_server
from cloudmesh_common.util import cond_decorator
from flask import Blueprint, g, render_template, request
import cloudmesh
from pprint import pprint
from cloudmesh.iaas.openstack.cm_compute import openstack
from cloudmesh_common.logger import LOGGER
import json

log = LOGGER(__file__)

pie_chart_fg380_module = Blueprint('pie_chart_fg380_module', __name__)

#
# ROUTE: PIE_CHART
#


@pie_chart_fg380_module.route('/pie_chart_fg380/<cloud>/', methods=['GET', 'POST'])
def profile(cloud):

    attributes = ['Cores', 'FloatingIps', 'Instances', 'RAM', 'SecurityGroups']
    max_attributes = ['maxTotalCores', 'maxTotalFloatingIps',
                      'maxTotalInstances', 'maxTotalRAMSize', 'maxSecurityGroups']
    used_attributes = ['totalCoresUsed', 'totalFloatingIpsUsed',
                       'totalInstancesUsed', 'totalRAMUsed', 'totalSecurityGroupsUsed']
    config = cm_config()
    o = openstack(cloud)
    limits = o.get_limits()
    data = {}
    for a, m, u in zip(attributes, max_attributes, used_attributes):
        x = json.dumps(a)
        data[x] = []
        data[x].append(['a', 'b'])
        data[x].append(
            ['available', limits['absolute'][m] - limits['absolute'][u]])
        data[x].append(['used', limits['absolute'][u]])
        data[x] = json.dumps(data[x])
    return render_template('pie_chart.html',
                           data=data,
                           cloud=cloud
                           )


'''
    u'maxImageMeta': 128,
               u'maxPersonality': 5,
               u'maxPersonalitySize': 10240,
               u'maxSecurityGroupRules': 20,
               u'maxSecurityGroups': 10,
               u'maxServerMeta': 128,
               u'maxTotalCores': 20,
               u'maxTotalFloatingIps': 10,
               u'maxTotalInstances': 10,
               u'maxTotalKeypairs': 100,
               u'maxTotalRAMSize': 51200,
               u'totalCoresUsed': 4,
               u'totalFloatingIpsUsed': 2,
               u'totalInstancesUsed': 2,
               u'totalRAMUsed': 8192,
               u'totalSecurityGroupsUsed': 0},
'''
