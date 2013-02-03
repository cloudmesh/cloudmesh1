#! /usr/bin/python

# https://www.windowsazure.com/en-us/develop/python/how-to-guides/service-management/

#from azure import *
#from azure.servicemanagement import *

#subscription_id = '<your_subscription_id>'
#certificate_path = '<path_to_.pem_certificate>'

#sms = ServiceManagementService(subscription_id, certificate_path)

#http://amoffat.github.com/sh/

#from sh import Command

#azure = Command('azure')

from sh import azure, sudo
import os


#print (azure("help"))



#os.system ("azure config list")

#print "------------"
#print (azure("config", "list"))
#print "------------"

#azure("account", "download")

#broken not sudo: azure("account", "import", "/Users/new/azure/.publishsettings")

#os.system ("sudo azure account import ~/azure/.publishsettings")

#azure("vm", "image", "list")

#os.system ("sudo azure vm image list")

#print (sudo.azure("vm","image","list"))

# create cert
#Country Name (2 letter code) [AU]:US
#State or Province Name (full name) [Some-State]:INDIANA
#Locality Name (eg, city) []:BLOOMINGTON
#Organization Name (eg, company) [Internet Widgits Pty Ltd]:IU
#Organizational Unit Name (eg, section) []:
#Common Name (eg, YOUR name) []:Gregor von Laszewski    
#Email Address []:laszewski@gmail.com
#os.system("openssl req -x509 -nodes -days 365 -newkey rsa:1024 -keyout mycert.pem -out mycert.pem")
#os.system("openssl x509 -inform pem -in mycert.pem -outform der -out mycert.cer")

def create_cert(name,organization,city,state,country,certname):
    # creates a cert file with the given common name information int
    # the files certname.pem and certname.cer
    #create cn
    data = {}
    data['certname']=certname
    data['name']=name
    data['organization']=organization
    data['state']=state
    data['country']=country
    data['city']=country
    data['cn'] ="/CN=%(name)s/O=%(organization)s/C=%(country)s/ST=%(state)s/L=%(city)s" % data
    #os.system("openssl req -x509 -subj \"/CN=Gregor von Laszewski/O=IU/C=US/ST=Indiana/L=Bloomington\"  -nodes -days 365 -newkey rsa:1024 -keyout mycert.pem -out mycert.pem")
    command = "openssl req -x509 -subj \"%(cn)s\"  -nodes -days 365 -newkey rsa:1024 -keyout %(certname)s.pem -out %(certname)s.pem" % data
    print command
    os.system(command)
    command = "openssl x509 -inform pem -in %(certname)s.pem -outform der -out %(certname)s.cer" % data
    print command
    os.system(command)

create_cert("Gregor von Laszewski","IU","Bloomington","Indiana","US","mycert")
