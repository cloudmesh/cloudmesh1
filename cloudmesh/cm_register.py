
class cm_register:

    def __init__(self, collection="cloudmesh"):

        self.db_clouds = get_mongo_db(collection)


   cm_kind = "clouds" # look up if this exists in the collection "cloudmesh"

   # if not we can use it, if it does we need a different one such as 

   # cm_kind = "clouds"
   # cm_id = "{0}-{1}".format(cloudname,cm_kind)
   # put the cloud info in that so you can find it 

   clouds = db_clouds.find ({"cm_kind" : "clouds"})

   than you can iterate over clouds 

   we want add method while a dict is the parameter to add
   the dict containes the cm_ thingys just as the other objects ... this may be more than just cm_kind
   ...
   refresh gregor with what the other opbjects have in them ....

   def list(cloud_name=None)

   def remove(cloud_name=None)

   if none, all of the clouds, we may not want to do this for remove .... ???


   d = 

 india_openstack_tetst:
            cm_kind: cloud
            cm_host: india.futuregrid.org
            cm_heading: India OpenStack, Havana
            cm_label: ios_havana
            cm_type: openstack
            cm_type_version: havana
            credentials:
                OS_AUTH_URL: https://i57r.idp.iu.futuregrid.org:5000/v2.0
                OS_CACERT: /home/cloudmesh/.futuregrid/india-havana-cacert.pem
                OS_VERSION: havana
            default:
                flavor: None
                image: None

   def add(cloudname, d)


main

  mesh = cm_register(filename="/cloudmesh.yaml")

  banner("LIST")
  mesh.list()

  banner("REMOVE")

  mesh.remove("india_openstack_test")
  mesh.list()

  banner("ADD")

  mesh.add("india_openstack_testb", d)
  mesh.list()

  banner("DONE")
