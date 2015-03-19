"""
::


    terminal1>
    $ python rest.py

    terminal2>
    $ curl "http://localhost:5000/v1.0/queue?resource=india.futuregrid.org"
    $ curl "http://localhost:5000/v1.0/queue?resource=india.futuregrid.org&id=1902410.i136"
    $ curl "http://localhost:5000/v1.0/queue/info?resource=india.futuregrid.org&queue=systest"


"""
from cloudmesh.pbs.pbs import PBS
from cloudmesh.pbs.pbs_mongo import pbs_mongo

from cloudmesh_base.ConfigDict import ConfigDict
from pprint import pprint

from flask import Flask, jsonify
from flask.ext import restful
from flask.ext.restful import reqparse
from cloudmesh_base.locations import config_file

version = "v1.0"

provider = PBS
# provider = pbs_mongo

app = Flask(__name__)
api = restful.Api(app)

queue_stat_parser = reqparse.RequestParser()
queue_stat_parser.add_argument('resource', type=str, required=True)
#queue_stat_parser.add_argument('user', type=str)
queue_stat_parser.add_argument('id', type=str)

queue_info_parser = reqparse.RequestParser()
queue_info_parser.add_argument('resource', type=str, required=True)
#queue_info_parser.add_argument('user', type=str)
queue_info_parser.add_argument('queue', type=str)

config = ConfigDict(
    prefix="cloudmesh", filename=config_file("/cloudmesh.yaml"))
user = config.get("cloudmesh.profile.username")


def versioned_url(url):
    return "/" + version + url


def simple_error(kind, attribute, help="does not exist"):
    msg = {}
    msg["error:"] = "{0} {1} {2}".format(kind, attribute, help)
    return msg


class rest_queue_stat(restful.Resource):

    def get(self):
        args = queue_stat_parser.parse_args()
        resource = args['resource']
        id = args['id']
        pbs = provider(user, resource)
        try:
            result = pbs.qstat()
        except:
            # 404
            return simple_error("resource", resource, help="connection refused"), 200

        if id is None:
            try:
                return jsonify({resource: result[resource]})
            except:
                return simple_error("resource", resource), 200   # 404
        else:
            try:
                return jsonify({id: result[resource][id]})
            except:
                return simple_error("id", id), 200    # 404


class rest_queue_info(restful.Resource):

    def get(self):
        args = queue_info_parser.parse_args()
        resource = args['resource']
        queue = args['queue']
        pbs = provider(user, resource)
        try:
            result = pbs.qinfo()
        except:
            # 404
            return simple_error("resource", resource, help="connection refused"), 200

        if queue is None:
            try:
                return jsonify({resource: result[resource]})
            except:
                return simple_error("resource", resource), 200   # 404
        else:
            pprint(result[resource])

            try:
                return jsonify({queue: result[resource][queue]})
            except:
                return simple_error("id", id), 200    # 404


api.add_resource(rest_queue_stat, versioned_url('/queue'))
api.add_resource(rest_queue_info, versioned_url('/queue/info'))

if __name__ == '__main__':
    app.run(debug=True)
