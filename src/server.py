import cherrypy
import os
from sh import cat
from sh import cm 

class CloudMeshServer(object):

    @cherrypy.expose
    def index(self):
        os.system("cm r")
        buttons = self.buttons()
        table = cat("/tmp/gvonlasz/cm.html")
        return buttons + str (table)

    @cherrypy.expose
    def refresh(self):
        return self.index()

    @cherrypy.expose
    def delete(self):
        os.system("cm kill")
        return self.refresh()

    @cherrypy.expose
    def reindex(self):
        os.system("cm reindex")
        return self.refresh()

    @cherrypy.expose
    def start(self, i):
        os.system("cm start:%s" % int(i))
        return self.refresh()

    @cherrypy.expose
    def par(self, i):
        os.system("cm par:%d" % int(i))
        return self.refresh()

    def buttons(self):
        r = "<a href=\"http://127.0.0.1:8080/\" class=\"button\">Refresh</a>"
        r += "<a href=\"http://127.0.0.1:8080/start/1\" class=\"button\">Add Instance</a>"
        r += "<a href=\"http://127.0.0.1:8080/reindex\" class=\"button\">Reindex</a>"
        r += "<a href=\"http://127.0.0.1:8080/delete\" class=\"button\">Delete</a>"
        r += "<br>"
        return r


cherrypy.quickstart(CloudMeshServer())
