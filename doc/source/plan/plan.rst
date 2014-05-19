.. |jira| replace:: https://jira.futuregrid.org/browse/FG-1418 
.. |JIRA| replace:: https://jira.futuregrid.org/browse/FG-


Plan: Cloudmesh Service Shift
======================================================================

.. contents:: Table of Content

Project Objectives
----------------------------------------------------------------------

|jira|

|JIRA|1418

:issue:`{issue.title} (#{issue.id}) <FG-1418>`

#FG-1418

Currently the FG RAIN service contains a service shift mechanism. We
like to further develop this mechnism by introducing an abstraction
for bare metal provisioning so that teefaa as well as OpenStack bare
metal provisioning can be used.  Services we target are Eucalyptus,
OpenStack, and HPC via SLURM (or Moab).

Development Objectives
----------------------------------------------------------------------

#. Develop a service that allows the reassignment of servers in a
   cluster to be used either as part of an HPC or Cloud IaaS
   farmework.

#. Make the service as much as possible independent through
   abstractions from services such as XCAT and Moab (which is
   currently not the case)

#. provide a simple Web based GUI for administrators to the service
   shift functionality

Production Objectives
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#. Verify what is in production and what is not

#. Continue the ongoing production of FG Move (it is unclear if it
   still in production)

#. Clarify the position of Teefaa in the production software

#. Introduce the new developments intop production

#. Reuse DevOps as part of the development and production efforts

Project Deliverables
----------------------------------------------------------------------

Test

Note this table will be adapted as part of our agile development
methodology. Once we agree on tasks they will be filed in jira

.. csv-table:: Development Tasks
    :header: "No.","<-","Task","Delivery","Staffing","Description","Jira"
    :widths: 2,2,10,3,5,30,3

    "1", "1", "Plan and Task Completion", "ongoing", "All", "If you detect any
    issues with the plan we need to address them quickly and adapt in
    agile fashion as we have done previously.", "TBD"
    "2", "1", "Agile Project meeting", "daily", "All", "A daily meeting to assure
    we are on track with the project. 10 minutes max, on google
    hangout. Just status updates and correcting plans.", "TBD" 
    "3", "4", "OpenStack BareMetal Test", "06/30", "Tanaka", "Deliver a Grizzly
    OpenStack with bare metal provisioning on a test cluster with at
    least 4 servers. Ideally would be 8", "TBD"
    "5", "3", "OpenStack BareMetal Production", "07/20", "Tanaka", "Deliver a Grizzly
    OpenStack with bare metal provisioning on part of India with at
    least 16 servers so we can test this in production.", "TBD"
    "6", "1", "Inventory", "06/30", "Streib, Laszewski","Deliver the inventory service inclusing a first flask framework
    to display the content of the inventory and integration to CMD3.", "TBD"
    "7.1", "6", "Shift Openstack service nodes", "07/30", "Streib,
    Tanaka, Laszewski","Deliver the shifting commandline abstraction that uses the
    OpenStack service nodes.", "TBD"
    "7.2", "6", "Shift Eucalyptus service nodes", "07/30", "Streib,
    Tanaka, Laszewski","Deliver the shifting commandline abstraction that uses the
    Eucalyptus service nodes.", "TBD"
    "7.3", "6", "Shift HPC service nodes", "07/30", "Streib,
    Tanaka, Laszewski","Deliver the shifting commandline abstraction that uses the
    HPC service nodes.", "TBD"


.. csv-table:: Production Oriented Tasks
    :header: "No.","<-","Task","Delivery","Staffing","Description","Jira"
    :widths: 2,2,10,3,5,30,3

    "4", "1", "Teefaa Production", "06/20", "Tanaka", "Clarify the use of
    Teefaa in Production in regards to Teefaa used in FGMove and
    Teefaa without FGMove. Put in production and interact with the
    team.", "TBD"
    "8", "1", "RAIN Production", "06/30", "Wang, Tanaka","Make sure the
    current RAin is in production.", "TBD"
    "9", "8", "RAIN Move", "06/30", "Wang, Tanaka","Identif the
    current state of FG Move and bring in production if we identify it
    to be useful.", "TBD"
    "10","all", "Demonstration", "08/30", "All", "Demonstrate Cloud
    Shifting of HPC, Eucalyptus and OpenStack services", "TBD"
    "11","1","RAIN Hardware Broken", "06/20","Tanaka", "Fixing the hardware issues on the
    machines for RAIN", "TBD"



Evolution of the Project
----------------------------------------------------------------------

The use of the outdated Moab and XCAT tools used in our production
environment to support FG RAIN makes it necessary to generalize the
approach to become independent from thes efforts. An important aspect
of this is the bare metal provisioning. New tools and services have
become recently available for example through OpenStack bare metal 
distributed in Grizzly that it is imperative to integrate such tools
into our solution and pproduction strategy. As such tools could evolve
we hope to provide a simple abstraction on top of bare metal
provsiioning that makes it easier for us to integrate with future
efforts. Furthermore, we hopw to leverage from existiong DevOps
frameworks to simplify development and reduce the time for deployment.

Refernce Materials
----------------------------------------------------------------------

FG Move:
    http://futuregrid.github.io/rain-move/

FG Rain:
    http://futuregrid.github.io/rain/

Teefaa:
    http://futuregrid.github.io/teefaa/

Inventory:
    http://futuregrid.github.io/inventory
    https://github.com/futuregrid/inventory

Flask_cm:
    http://futuregrid.github.io/flask_cm
    https://github.com/futuregrid/flask_cm


Definitions and Acronyms
----------------------------------------------------------------------

FG Rain (in production?, Hardware Issues?):
   FutureGrid Rain is a tool that will allow users to place customized
   environments like virtual clusters or IaaS frameworks onto
   resources. The process of raining goes beyond the services offered
   by existing scheduling tools due to its higher-level toolset
   targeting virtualized and non-virtualized resources. Rain will be
   able to move resources from one infrastructure to another and
   compare the execution of an experiment in the different supported
   infrastructures.

FG Move (in production?, Hardware issues?):  
   is a service that enables physical resources re-allocation among
   infrastructures. By using a simple command line interface, this
   service is able to de-register a machine from a particular
   infrastructure and register it in another one. Internally, this
   service makes use of Teefaa to dynamically provision the selected
   machine with the OS and software needed for a successful
   registration in the new infrastructure. FG Move also maintains a
   database with information about the machines composing each one of
   the different infrastructures. The database can be consulted to
   obtain detailed information about a particular infrastructure.

Teefaa: 
    (to be verified) The definition of what teefaa is has been
    changing over time thus we need as part of this plan to identify
    more clearly what it is. We have a number of different versions of
    Teefaa that are currently used and/or developed.

Teefaa 1 (in production, TBD?):
     In the first version of teefaa the focus was layed on bare metal
     provisioning of the OS while utilizing the scheduling system. As
     we wanted to be independent from XCAT and MOAB this was achieved
     by integrating it into TORQUE. Teefaa is used as part of FG Move.

Teefaa 2 (status TBD):
     Teefaa was enhanced to integrate a mechnism for developing an
     image on a local laptop so that the image can than be snapshotted
     and placed onto a cluster so that bare metal provisioning can be
     achieved from this image. Based on previous conversation 
     this verasin was or is installed in some fashion on India. A
     clarification is needed.

Teefaa 3 (status TBD):
      Much of Teefaa 2 was developed mostly in shell, some aspects of
      it are developed better in python. Teefaa 3 provides an attempt
      to deliver a mostly python based implementation. It is unclear
      if this code has been used or is installed on india. This
      version of teefa uses a self written subprocess handler that
      exists already via others.

Teefaa 4 (status TBD):
      Much of Teefaa 2 was developed mostly in shell, some aspects of
      it are developed better in python. Teefaa 4 provides an attempt
      to deliver a mostly python based implementation. It is unclear
      if this code has been used or is installed on india. Some
      bittorrent functionality to distribute images are included and
      the use of fabric which is heavily used by cloudmesh developers
      is introduced. Fabric as is may have some scaleblity problems,
      but we will not hit them with our small clusters.
     
Cloudmesh Inventory: 
      FG Move contains a simple inventory that is not suffcient to
      deal with all of our needs. Cloudmesh inventory separates the
      code base from FG move to make it independent and adds new
      features to it.

Cloudmesh Service Shift:
      Currently the FG RAIN service contains a service shift
      mechanism. We like to redevelop this mechnism by introducing an
      abstraction for bare metal provisioning so that teefaa as well
      as OpenStack bare metal provisioning can be used.
      Services we target are Eucalyptus, OpenSTack, and HPC via SLURM
      (or Moab).

      	  

