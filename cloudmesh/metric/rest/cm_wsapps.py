import os
from flask import Flask, jsonify
from flask.views import View
from FGMimerender import mimerender
# from fgmetric.shell.FGDatabase import FGDatabase


class ListVMs(View):

    def __init__(self):
        self.db = FGDatabase()
        self.db.conf()
        self.db.connect()
        self.cloudservice = None
        self.data = None

    @mimerender
    def dispatch_request(self):
        self.read_cloud_service()
        self.read_vms()
        res = self.data
        return {"message": res}

    def read_cloud_service(self):
        res = self.db.read_cloudplatform()
        new_res = {}
        for cloud in res:
            new_res[cloud['cloudPlatformId']] = cloud
        self.cloudservice = new_res

    def read_vms(self):
        cursor = self.db.cursor
        table = self.db.instance_table
        table2 = self.db.cloudplatform_table
        query = "select %(table2)s.platform as CLOUDNAME, DATE_FORMAT(date, '%%Y %%b') as 'MONTH YEAR', count(*) as VALUE from %(table)s, %(table2)s group by %(table2)s.platform, YEAR(date), MONTH(date)" % vars(
        )

        try:
            cursor.execute(query)
            self.data = cursor.fetchall()
        except:
            print sys.exc_info()

    def map_cloudname(self):
        for record in self.data:
            try:
                cloudname = self.cloudservice[record['cloudplatformidref']]
            except:
                print record

app = Flask(__name__)
app.add_url_rule('/list_vms.json', view_func=ListVMs.as_view('list_vms'))

if __name__ == "__main__":
    app.run(host=os.environ["FG_HOSTING_IP"], debug=True)
