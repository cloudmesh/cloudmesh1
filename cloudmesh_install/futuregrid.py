from cloudmesh_base.util import banner
from cloudmesh_base.locations import config_file
from paramiko import SSHClient, AutoAddPolicy, BadHostKeyException
from paramiko import AuthenticationException, SSHException
import sys
import os
import stat
import getpass
import glob
import yaml
from string import Template
from docopt import docopt
from ConfigParser import SafeConfigParser
from pprint import pprint

rc_file_locations = {
    'india': {
        'hostname': 'india.futuregrid.org',
        'source': '.futuregrid/openstack_havana/novarc',
        'dest': "~/.cloudmesh/clouds/india",
    }

    # NEW ICEHOUSE
    # ,
    # 'icehouse': {
    # 'hostname': 'india.futuregrid.org',
    # 'source': '.cloudmesh/clouds/india/icehouse/novarc'
    # ' .cloudmesh/clouds/india/icehouse/cacert.pem',
    # 'dest': "~/.cloudmesh/clouds/icehouse",
    # }
}


def iu_credential_fetch_command(args):
    """
    Usage:
            cm-iu -h | --help
            cm-iu user fetch [--username=USERNAME] [--outdir=OUTDIR]
            cm-iu user create
            cm-iu user login [--username=USERNAME]
    """

    _args = ' '.join(args[1:])
    arguments = docopt(iu_credential_fetch_command.__doc__, _args)

    if arguments["user"] and arguments["fetch"]:
        fetchrc(arguments["--username"], arguments["--outdir"])

    elif arguments["user"] and arguments["create"]:
        apply_credentials_to_yaml_file()

    elif arguments["user"] and arguments["login"]:
        verify_ssh_login(arguments["--username"])

def download_rc_files(userid):

    for hostname in rc_file_locations:
        host = rc_file_locations[hostname]
        host["userid"] = userid
        host["dest"] = os.path.expanduser(host["dest"])

        print "fetching from ", host["hostname"],
        pprint (host)
        print "create directory:", "%(dest)s" % host

        os.system("mkdir -p %(dest)s" % host)

        copy_cmd = "scp -o StricthostKeyChecking=no %(userid)s@%(hostname)s:%(source)s %(dest)s" % host
        print "    <-", copy_cmd
        print "    ",
        result = None
        try:
            from sh import scp
            result = scp("-o", "StrictHostKeyChecking=no",
                         "%(userid)s@%(hostname)s:%(source)s" % host, "%(dest)s" % host)
            print "ok", result
        except Exception, e:
            print "failed", result, e


def apply_credentials_to_yaml_file():
    """
    rc_dir_location = {}
    # (hostname, loaction of dir on remote host, location of dir on localhost)
    rc_dir_location["india"] = ("india.futuregird.org", "?", "?")

    for label in rc_dir_location
        (host,dir) = rc_rdilocation(label)
        get rc file form the host and dir and copy to install_dir

    me_dict = read current me.yaml



    for label in rc_dir_location
        (host,dir) = rc_rdilocation(label)

        if label does not exist make it and also add the credentials for it,
            fill out initially with TBD

        if openstack:
           put values from local dir into dict

        elif eucalyptus:
           put values from local dir into dict

    return me dict
    """

    class Readrcfile(object):

        """ Read novarc, eucarc and store variables
            with configparser
            reference:
            http://stackoverflow.com/questions/2819696/parsing-properties-file-in-python/2819788#2819788
        """

        def __init__(self, fp):
            self.fp = fp
            self.head = '[rcfile]\n'

        def readline(self):
            if self.head:
                try:
                    return self.head
                finally:
                    self.head = None
            else:
                return self.fp.readline().replace("export ", "")

    def get_variables(fpath):
        section_title = "rcfile"
        # case-sensitive
        read_values = ["OS_TENANT_NAME", "OS_USERNAME", "OS_PASSWORD"]
        result = {}

        cp = SafeConfigParser()
        try:
            cp.readfp(Readrcfile(open(fpath)))
            # cp.items(section_title)
            for read_value in read_values:
                tmp = cp.get(section_title, read_value)
                if tmp.startswith("$"):
                    tmp = cp.get(section_title, tmp[1:])  # without $ sign
                result[read_value] = tmp
            return result

        except:
            print "ERROR: Failed to read rc files. Please check you have valid \
                    rcfiles in %s." % fpath
            print sys.exc_info()
            sys.exit(1)

    # #######################################################
    # MISSING PART IS HERE
    # WE HAVE TO FILL THE me.yaml FILE WITH A REAL VALUE HERE
    # #######################################################

    # me-all.yaml is correct one instead me-none.yaml
    # to fill variables with template
    # -----------------------------------------------

    dir = config_file("")
    me_file = dir + "/me.yaml"

    try:
        result = open(me_file, 'r').read()
        values = yaml.safe_load(Template(result).substitute(os.environ))
    except Exception, e:
        print "ERROR: There is an error in the yaml file", e
        sys.exit(1)

    # rcfile location
    rcfile_path = dir + "/clouds/"
    new_values = {}
    for filepath in glob.glob(rcfile_path + "/*/*rc"):
        filename = os.path.basename(filepath)
        cloud_name = os.path.basename(
            os.path.normpath(filepath.replace(filename, "")))
        new_values[cloud_name] = get_variables(filepath)
        print "Reading  -> %s" % filepath

    for cloud in values['clouds']:
        values['clouds'][cloud]['default'] = {}
        # Fill in credentials with real values
        # This does not update me.yaml file. This will be done soon.
        try:
            for k, v in new_values[cloud].iteritems():
                values['clouds'][cloud]['credential'][k] = new_values[cloud][k]
        except:
            pass

    cloudmesh_out = dir + '/cloudmesh.yaml'

    # file_from_template
    # ------------------
    # This is only for replacing variables in Jinja2 template.

    # For example, {{clouds.openstack.credential}} is going to be replaced with
    # values['clouds']['openstack']['credential']

    # file_from_template(cloudmesh_out, cloudmesh_out, values)

    # replace TBD in yaml
    # -------------------
    # 'cm-init fill' might do same thing
    #
    # In case yaml file contains TBD values, this logic replaces it with real
    # values
    # Similar to file_from_template but replace with TBD
    try:
        result = open(cloudmesh_out, 'r').read()
        data = yaml.safe_load(Template(result).substitute(os.environ))
    except Exception, e:
        print "ERROR: There is an error in the yaml file", e
        sys.exit(1)

    # Update yaml if a value is TBD
    # -----------------------------
    # 'cm-init fill' might do same thing
    for cloud_name, value in new_values.iteritems():
        clouds_in_yaml = data['cloudmesh']['clouds']
        if cloud_name in clouds_in_yaml:
            credentials = clouds_in_yaml[cloud_name]['credentials']
            for k, v in value.items():
                if k in credentials and credentials[k] == "TBD":
                    credentials[k] = v

    # replacing default project and username
    data['cloudmesh']['hpc']['username'] = new_values[
        cloud_name]['OS_USERNAME']
    data['cloudmesh']['profile']['username'] = new_values[
        cloud_name]['OS_USERNAME']
    data['cloudmesh']['projects']['default'] = \
        new_values[cloud_name]['OS_TENANT_NAME']
    # active projects can be multiple values
    # it should be a list to stack unique project ids
    # TBD
    data['cloudmesh']['projects']['active'] = \
        [new_values[cloud_name]['OS_TENANT_NAME']]

    # Write yaml
    with open(cloudmesh_out, 'w') as outfile:
        #
        # TODO: this is wrong as it should probably use cm_config and the write method in it
        # to preserve order
        #
        outfile.write(yaml.dump(data, default_flow_style=False, indent=4))
        print "Updating -> %s" % cloudmesh_out


def fetchrc(userid=None, outdir=None):

    banner("download rcfiles (novarc, eucarc, etc) from IaaS platforms")

    print ""
    # Task 1. list portal user id

    '''
    try:
        from cloudmesh_base.ConfigDict import ConfigDict
    except Exception, e:
        print "ERROR: your have not yet configured cloudmesh completely. "
        print "       Have you called"
        print
        print "          ./install cloudmesh"
        print
        sys.exit(1)

    dir = config_file("")

    config = ConfigDict(dir + "/me.yaml")
    userid = config["portalname"]
    '''

    if not userid:
        userid = getpass.getuser()
        userid = raw_input("Please enter your portal user id [default: %s]: " %
                           userid) or userid

    # Task 2. list hostnames to get access. In FutureSystems, india is default
    # TEMPORARY
    host_ids = ["india"]

    # user input is disabled
    # host_ids = raw_input("Please enter host identifications [default: %s]: "
    #                     % ", ".join(host_ids)) or host_ids

    if isinstance(host_ids, str):
        host_ids = map(lambda x: x.strip(), host_ids.split(","))

    # domain_name = ".futuregrid.org"
    # hostnames = map(lambda x: x.split("_")[0] + domain_name, host_ids)

    # key_path = "~/.ssh/id_rsa"
    # private key path is disabled
    # key_path = raw_input("Please enter a path of the ssh private key to" + \
    #                     " login the hosts [default: %s]: " % key_path) or \
    #                    key_path

    try:

        download_rc_files(userid)
        update_permission("~/.cloudmesh/clouds")

        """
        # cmd = "fab rcfile.download:userid='%s',host_ids='%s',key_path='%s'" \
        cmd = "fab -H %s -u %s -i %s rcfile.download:'%s','%s'" \
            % (",".join(hostnames), userid, key_path,
               "\,".join(host_ids), outdir)
        print "CMD", cmd
        os.system(cmd)
        """

    except:
        print sys.exc_info()
        sys.exit(1)


def update_permission(path, mode=stat.S_IRWXU):
    """Update file permissions on a given path."""
    os.chmod(os.path.expanduser(path), mode)
    for item in glob.glob(os.path.expanduser(path) + "/*"):
        os.chmod(os.path.join(path, item), mode)
        if os.path.isdir(item):
            update_permission(os.path.join(path, item), mode)


def verify_ssh_login(userid):
    client = SSHClient()
    client.load_system_host_keys()
    # client.set_missing_host_key_policy(WarningPolicy)
    client.set_missing_host_key_policy(AutoAddPolicy())

    # TEST ONLY
    hosts = ["india.futuregrid.org"]
    key = os.path.expanduser(os.path.join("~", ".ssh", "id_rsa"))
    print "[key: %s]" % key

    if not userid:
        userid = getpass.getuser()

    for host in hosts:
        try:
            client.connect(host, username=userid, key_filename=key)
            client.close()
            print "[%s] succeeded with %s." % (host, userid)
        except (BadHostKeyException,
                AuthenticationException,
                SSHException) as e:
            # print sys.exc_info()
            print ("[%s] %s with %s. Please check your ssh setup (e.g. key " +
                   "files, id, known_hosts)") % (host, e, userid)


def main(args=sys.argv):
    iu_credential_fetch_command(args)

if __name__ == '__main__':
    main(sys.argv)
