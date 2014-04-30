Cloudmesh Shell Rain 
=====================

Rain provides the elementary functionality to enable bare metal provisioning for compute resources. To find out more about the command you can say::

  cm> rain -help

This will print you a help message about the rain command.

Managing Servers/hosts
-------------------------

To add hosts to the system we can use either ``.json`` or ``.cfg`` files. The file extension will indicate which format is chosen. Thus we can add resources with:: 

  cm> rain --add -label i001 -file spec.json

and::

  cm> rain --add -file spec.json

Adding hosts can be augmented with a label option to overwrite the label information specified in the file. However in this case there must only be one host defined in the json file. In case multiple hosts are defined the label must be defined within each host object.

In case you like to use a n attribute name pair defining the objects, you can do so. Multiple entries are separated by an empty line in this case::

  cm> rain --add host -file spec.cfg

.. note::

	include here details of file with attribute:value

::

  cm> rain --enable -label i001

adds to the bare metal provisining machines the machine identified in the inventory by the label i001

Sometimes it may be necessary to delete a specific host. This can be done by deleting it by label. Host lists can be used as a parameter. Thus::

  cm> rain --delete -label i001

would delete the host with the label001 and::

  cm> rain --delete -label “i001-i03,i007” 

would delete hosts i001,i002, i003, and i007.

In some cases you may wish to remove the ability of a host to conduct bare metal provisioning all together, or enable it if it was previously disabled.::

  cm> rain --disable -label i001

would disable the host with the label i001 for bare metal provisioning. The disable and enable command can also specify host lists::

  cm> rain --disable -label “i001-i010” 

To enable host you can say:: 

  cm> rain --enable -label “i001-i010” 
  cm> rain --enable -label “i001-i010” 

.. note::
   
   shoule we use rain --on for rain --enable and rain --off for disable ?

The enable and disable commands are restricted to the users with administrative role. No other user can enable and disable hosts. 

Naturally we also want to see a list of hosts and their attributes. You can specify the return format to json or cfg. This can be done either by setting a prefered return format in the shell with::

  cm> set format=json 

and than using the command::

  cm> rain -list 

or specifying it explicitly to overwrite the default::

  cm> rain -list --format json

::
  
  cm> rain -list --format cfg

To retrieve a specific set of nodes one can use a hostlist as parameter to the label argument::

  cm> rain --list -label i001-i003

which then returns the information of the hosts with label i001, i002, and i003. To retrieve the information about a specific host we just use a specific host label as part of the label parameter such as::

  cm> rain --list -label i001

User, Project and Role Policies
---------------------------------

An important aspect of rain is that bare metal provisioning of resources is defined by projects, roles, or usernames. policies can be easily defined. For example the command::

  cm> rain -label i001-i003 -policy users=gregor,fugang,heng

will give the users gregor, heng and fugang the right to bare metal provision the resources i001, i002, and i003. The users must coordinate among themselves how to use bare metal provisioning on them.

In the same way we can define to grant access by project. Thus the command::

  cm> rain -label i001-i003  -policy projects=fg82,fg355

will grant all users from project fg82 and fg355 bare metal provisioning access to the thre hosts. 

Setting user policies is only allowed by the administrator. Please note that a policy may overwrite another policy. for a given node

.. note:: 

	roles are not yet supported

In addition to users and project, we can also define policies by roles. An administrator cen define arbitrary roles and add users and projects to the roles, while using regular expressions, thus I can define users for a particular role. An example would be::

  cm> rain --role group_a -rule “(project=fg82,fg355) and not (user=gregor,fugang)”

This would define a group of users that contains all users from project fg82 and fg355, but not the user gregor and fugang. Please note that hostlists are used to define the attributes. Thus I also could say “project=fg10-fg100” to indicate all projects between these project numbers. Also note that I can use the attributes as many times as I like in the regular expression.

Once a role is defined I can use it as part of our bare metal provisioning policies. Thus the command::

  cm> rain -label i001-i003  -policy role=group_a

would define that the three resources can be provisioned by the users identified by the role specifying group_a

Information 
-------------

Once policies are defined it is often a good idea to return information about it. Thus the command:: 

  cm> rain -list -projects fg82

Would return all host that project fg82 has control over. Howvefer if the user executing this command is not in project fg82, he will get a message that he is not authorized to retrieve this information.

To see all policies for for a user using the shell, he could just use the command::

  cm> rain -list 

Which provides an overview about which hosts the use logged into ``cm`` can use.

Naturally administrators can see more information, thus the command::

  cm> rain -list -projects

lists all projects that have access to bare metal and its servers. And::

  cm> rain -list -users

lists all servers that can be provisined by user

Provisioning
------------

Now that we know how to manage access to bare metal provisioning, we need to identify how to actually do it. The first thing we have to define is a rain descriptor that for example defines the operating system image, and how to start that image on the node. In case of centos, for example a kickstart file can be used.

Thus we can define a template such as::

  cm> rain template -label my-centos “-os centos -distro <imagename> -kickstart <kickstartname>”

Now we can reuse this template by specifying the hosts on which I try to apply the template. This is done with::

  cm> rain -host i001-i003 my-centos

To list the available templates you can say::

  cm> rain template -list

To list more information about a specific template, please just add the template name::

  cm> rain template -list my-centos

Status
---------

Naturally an important feature is to observe the status of the bare metal provisioning, where::

  cm> rain status 

lists me the status of all rain activities I do and::

  cm> rain status -label i001-i003 

limits the information to the three specified machines.

As this information may be plentiful, we have provides to the status command some reduced options. This includes::

  cm> rain status short

which prints out a 

| ``+`` for each resource for which raining succeeded, 
| ``-`` for each resource that has failed
| ``.`` for each resource that is still in progress and a the status is unkown

For hundrets of rain activities, this may be an important feature, NAturally the label attribute can be specified to restrict the hosts reported upon::

  cm> rain status short -label i001,i003

An alternative format is the summary format that simply list counts for the hosts in the various categories::

  cm> rain status summary -label i001,i020

prints something like::

  provisioned:  3
  failed:      10
  in progress:  7
  total:       20

Reservation Interface (extension)
---------------------------------

Our previous reservation was done in an unlimited fashion. However sometimes it is desirable to actually reserve a provisioning at a given time. This can be achieved while augmenting the policies with a time interval. Thus the command::

  cm> rain -label i001-i003 -policy users=gregor -start <time_start> -end <time_end>

::

  cm> rain -n 5 -policy users=gregor -start <time_start> -end <time_end>

will define a reservation of three hosts for the user gergor for the given time. An error will occur if this reservation can not be conducted during that time.
 
The time is specified in the following format yyyy/mm/dd hh:mm:ss

Please note that the definition of using seconds may not be implemented and due to recovering resources from others, may take some time. We are working towards padding reservations at the end so that they become very close available defined by the reservation.

Free resources can be identified by simply asking the list function and specifying the start and end times. Thus::

  cm> rain -list -start <time_start> -end <time_end> 

wil list me the available resources between thise time, note however that they may be restricted by additional policies and if so you will only get back resources that fulfill your user and project memberships. 

If you use the display option a nice image is create in the file with the given name::

  cm> rain -list display file.png

It is similar to a gantt chart showing resrevations by users, projects, and groups.

