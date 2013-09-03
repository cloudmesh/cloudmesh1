import yaml
import subprocess

class Migrate_MySQL_to_Mongo:

    def load_db_info(self):
        stream = open("dbinfo.yaml", "r")
        self.dbinfo = yaml.load(stream)
        #self.load_mysqldb_info()
        #self.load_mongodb_info()

    def load_mysqldb_info(self):
        self.mysqldb_userid = ""
        self.mysqldb_passwd = ""
        self.mysqldb_hostname = ""
        self.mysqldb_port = 3306
        self.mysqldb_dbname = ""
        self.mysqldb_tables = []

    def load_mongodb_info(self):
        self.mongodb_hostname = ""
        self.mongodb_userid = ""
        self.mongodb_passwd = ""
        self.mongodb_port = 27107
        self.mongodb_dbname = ""
        self.mongodb_collections = []

    def get_tables(self):
        return self.dbinfo["mysqldb_tables"]

    def export_mysql_in_csv(self, table):
        query = "select * from %s.%s" % (self.dbinfo["mysqldb_dbname"], table)
        cmd1 = "mysql -u %s -p%s -h %s -e \"%s\" --batch" % \
        (self.dbinfo["mysqldb_userid"],
         self.dbinfo["mysqldb_passwd"],
         self.dbinfo["mysqldb_hostname"],
         query)

        cmd2 = "sed 's/\t/\",\"/g;s/^/\"/;s/$/\"/;s/\n//g'" 

        p1 = subprocess.Popen(cmd1.split(), stdout=subprocess.PIPE)
        p2 = subprocess.Popen(cmd2.split(" "), stdin=p1.stdout,
                              stdout=subprocess.PIPE)

        output = p2.communicate()[0]
        print output

        p1.stdout.close()
        p2.stdout.close()

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
