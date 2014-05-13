import sys
from tabulate import tabulate
import requests

class metric_api:

    def __init__(self):
        self.from_date = None
        self.to_date = None
        self.period = None
        self.metric = None
        self.cluster = None
        self.iaas = None
        self.userid = None

        self.load_server_info()

    def __str__(self):
        result = ""
        result += "from_date: %s\n" % self.from_date
        result += "to_date:   %s\n" % self.to_date
        result += "period:    %s\n" % self.period
        result += "metric:    %s\n" % self.metric
        result += "cluster:   %s\n" % self.cluster
        result += "iaas:      %s\n" % self.iaas
        result += "userid:      %s\n" % self.userid
        return result

    def load_server_info(self):
        # cloudmesh_server.yaml contains the api server info
        # this is only for test.
        self.host = "156.56.93.202"
        self.port = 5001
        self.doc_url = "metric"
 
    def connect(self):
        try:
            print self.get_uri()
            r = requests.get(self.get_uri())
            return r.json()
        except requests.ConnectionError:
            print "Connection failed to %s" % self.get_uri()
        except requests.HTTPError as e:
            print "Invalid HTTP response ({0},{1})".format(e.errno, e.strerror)
        except requests.Timeout:
            print "HTTP times out"
        except requests.TooManyRedirects:
            print "Exceeds the configured number of maximum redirections"
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise

    def get_uri(self):
        # /metric/<cloudname>/<clustername>/<username>/<metric>/<timestart>/<timeend>/<period>
        uri = ["http:/"]
        uri.append(self.host + ":" + str(self.port))
        uri.append(self.doc_url)
        uri.append(self.iaas)
        uri.append(self.cluster)
        uri.append(self.userid)
        uri.append(self.metric)
        uri.append(self.from_date)
        uri.append(self.to_date)
        uri.append(self.period)
        self.uri = "/".join(map(str,uri))
        return self.uri
    
    def set_date(self, from_date, to_date):
        self.from_date = from_date
        self.to_date = to_date

    def set_period(self, period):
        self.period = period

    def set_metric(self, metric):
        self.metric = metric

    def set_cluster(self, cluster):
        self.cluster = cluster

    def set_iaas(self, cloud):
        self.iaas = cloud

    def set_cloud(self, cloud):
        ''' link to set_iaas '''
        self.set_iaas(cloud)

    def set_user(self, userid):
        self.userid = userid

    def test_raw_data(self):
        # for test, dummy data is returned
        res = [["HOST", "PROJECT", "cpu", "memory_mb", "disk_gb"],
               ["india","(total)",2, 4003,157],
               ["india","(used_now)", 3, 5120, 40],
               ["india","(used_max)",3,4608, 40],
               ["india","b70d90d65e464582b6b2161cf3603ced",1,512,0],
               ["india","66265572db174a7aa66eba661f58eb9e",2,4096,40]]
        return res
 
    def get_raw_data(self):
        # expect list variable
        res = self.connect()
        # res is dict
        dictlist = []
        i = 0
        for row in res["message"]:
            if i == 0:
                dictlist.append(row.keys())
            i=1
            dictlist.append(row.values())
        self.raw_data = dictlist

    def display(self, table_format="orgtbl"):
        # table_format = 
        # plain,
        # simple,
        # grid,
        # pipe,
        # orgtbl,
        # rst,
        # mediawiki,
        # latex
        self.table = tabulate (self.raw_data, headers="firstrow", tablefmt="orgtbl")
        seperator = self.table.split("\n")[1].replace("|", "+")
        print seperator
        print self.table
        print seperator        

        
    def get_stats(self):
        #print vars(self)
        self.get_raw_data()
        self.display("grid")
        return

    def stats(self):
        ''' link to get_stats '''
        return self.get_stats()
