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
        try:
            return self.dbinfo["mysqldb_tables"]
        except:
            return

    def export_mysql_in_csv(self, tablename):
        """Export mysql database tables using 'mysql' command line tools

        :param tablename: table name to export
        :type tablename: str

        """
        query = "select * from %s.%s" % (self.dbinfo["mysqldb_dbname"],
                                         tablename)
        res_mysql = mysql("-u", "{0}".format(self.dbinfo["mysqldb_userid"]),
                          "-p{0}".format(self.dbinfo["mysqldb_passwd"]),
                          "-h", "{0}".format(self.dbinfo["mysqldb_hostname"]),
                          "-e", "{0}".format(query),
                          "--batch")

        # Add quote(") at first
        # Then replace tab to ","
        # , add quote(") between new line
        # remove the last quote by [:-1] since \"\n\" adds dummy quote at last
        output = "\"" + str(res_mysql).replace("\t", "\",\"").replace("\n", "\"\n\"")[:-1]

        self.csv_data = output
        return output

    def mongoimport_csv(self, csv_data, tablename):
        """Import database data in a csv,json or tsv format using mongoimport
        command line tool.

        Reference: http://docs.mongodb.org/manual/reference/program/mongoimport/

        :param csv_data: database content to import
        :type csv_data: str.
        :param tablename: collection name for importing data
        :type tablename: str.

        """
        # mongoimport -u cmetrics_user -p -d cloudmetrics -c cloudplatform
        # -type csv -f fields-sep-by-coma --drop cloudplatform.csv --headerline
        mongoimport("-u", "{0}".format(self.dbinfo["mongodb_userid"]),
                    "-p", "{0}".format(self.dbinfo["mongodb_passwd"]),
                    "-d", "{0}".format(self.dbinfo["mongodb_dbname"]),
                    "-c", "{0}".format(tablename),
                    "-type", "csv",
                    "-f", "fields-sep-by-coma", "--headerline", "--drop",
                    _in=csv_data)

if __name__ == "__main__":
    migrate = Migrate_MySQL_to_Mongo()
    migrate.load_db_info()
    for tablename in migrate.get_tables():
        csv_data = migrate.export_mysql_in_csv(tablename)
        migrate.mongoimport_csv(csv_data, tablename)
