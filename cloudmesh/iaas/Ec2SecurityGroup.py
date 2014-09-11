#! /usr/bin/env python

# This class defines the security group that coud be potentially used by
# EC2 compatible cloud in general, e.g. AWS, OpenStack, Eucalyptus


class Ec2SecurityGroup(object):

    # Rules are defined based on protocol (TCP, UDP, ICMP), port range (from, to),
    # source ip address in cidr format.
    # A rule has to be part of a security group (parent_group_id)

    class Rule(object):

        def __init__(self, from_port, to_port, ip_protocol='tcp', cidr='0.0.0.0/0', parent_group_id=None):
            self.ip_protocol = ip_protocol
            self.cidr = cidr
            self.from_port = from_port
            self.to_port = to_port
            self.parent_group_id = parent_group_id

        # overload '==' comparison
        def __eq__(self, other):
            ret = False
            if isinstance(other, Ec2SecurityGroup.Rule) and\
               self.ip_protocol == other.ip_protocol and\
               self.cidr == other.cidr and\
               self.from_port == other.from_port and\
               self.to_port == other.to_port:
                ret = True
            return ret

        # '!=' comparison
        def __ne__(self, other):
            return not self.__eq__(other)

    # a security group must have a name, and optionally a description
    def __init__(self, name, description='generated via cloudmesh'):
        self.name = name
        self.description = description
        self.rules = []

    def set_rules(self, rules):
        self.rules = rules
