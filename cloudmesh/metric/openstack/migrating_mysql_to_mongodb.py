# -*- coding: utf-8 -*-
"""
    cloudmesh.metric.openstack.migrating_mysql_to_mongodb
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This module migrates mysql database to mongodb.

"""

import yaml
from sh import mysql
from sh import mongoimport

class Migrate_MySQL_to_Mongo:
    """The Migrate_MySQL_to_Mongo exports mysql database tables in a csv format,
    and pour into mongodb using mongoimport command line tools. The database
    information is loaded from 'dbinfo.yaml' file which contains db access
    information such as hostname, user name, and password.
    """

    def load_db_info(self):
        """Read database information such as hostname, user id, password, and
        database name"""
        stream = open("dbinfo.yaml", "r")
        self.dbinfo = yaml.load(stream)

    def get_tables(self):
        """Return mysql database tables to export"""
        return self.dbinfo["mysqldb_tables"]

    def export_mysql_in_csv(self, table):
        """Export mysql database tables using 'mysql' command line tools"""
        query = "select * from %s.%s" % (self.dbinfo["mysqldb_dbname"], table)
        cmd1 = "mysql -u %s -p%s -h %s -e \"%s\" --batch" % \
        (self.dbinfo["mysqldb_userid"],
         self.dbinfo["mysqldb_passwd"],
         self.dbinfo["mysqldb_hostname"],
         query)

        #cmd2 = "sed 's/\t/\",\"/g;s/^/\"/;s/$/\"/;s/\n//g'" 

        #p1 = subprocess.Popen(cmd1.split(), stdout=subprocess.PIPE)
        res_mysql = mysql("-u", "{0}".format(self.dbinfo["mysqldb_userid"]),
                          "-p{0}".format(self.dbinfo["mysqldb_passwd"]),
                          "-h", "{0}".format(self.dbinfo["mysqldb_hostname"]),
                          "-e", "\"{0}\"".format(query),
                          "--batch")

        #p2 = subprocess.Popen(cmd2.split(" "), stdin=p1.stdout,
        #                      stdout=subprocess.PIPE)

        # Add quote(") at first
        # Then replace tab to ","
        # , add quote(") between new line
        output = "\"" + str(res_mysql) \
                .replace("\t","\",\"") \
                .replace("\n","\"\n\"")

        #output = p2.communicate()[0]
        print output

        #p1.stdout.close()
        #p2.stdout.close()

    def mongoimport_csv(self, table):
        # mongoimport -u cmetrics_user -p -d cloudmetrics -c cloudplatform
        # -type csv -f fields-sep-by-coma --drop cloudplatform.csv --headerline
        filename = table + ".csv"
        cmd = "mongoimport -u %s -p %s -d %s -c %s -type csv -f \
        fields-sep-by-coma --drop %s --headerline" % \
                     (self.dbinfo["mongodb_userid"], 
                      self.dbinfo["mongodb_passwd"], 
                      self.dbinfo["mongodb_dbname"], 
                      table,
                      filename)
        subprocess.call(cmd.split())

if __name__ == "__main__":
    migrate = Migrate_MySQL_to_Mongo()
    migrate.load_db_info()
    for table_name in migrate.get_tables():
        migrate.export_mysql_in_csv(table_name)
        migrate.mongoimport_csv(table_name)
