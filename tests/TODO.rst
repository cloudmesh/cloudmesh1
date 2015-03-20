All I have added a simple example on how to do a cm command line test within nosetests. To do that I have developed a simple fgrep like function

how this works, you can now define your own functiions in test_shell and use the grep_command


	there are three parameters
	command = the actual cm command you like to execute
	first parameter is a list of strings that must be in the return from the command
	second parameter is a list of strings that must not be in the putput

	if you use None for one of the lists the list check is removed

def test_list(self):
    print
    a = self.grep_command("list", ["alamo", "india_openstack_havana"], None)


On Jul 17, 2014, at 9:34 AM, Gregor von Laszewski <laszewski@gmail.com> wrote:

bug: cm cloud

	we need to have a second column that adds the status of the cloud, e.g. if it is activated or not

	this is also the diffence to the list command. the list command lists apparently just the activated clouds.
	please double check



On Jul 17, 2014, at 7:44 AM, Gregor von Laszewski <laszewski@gmail.com> wrote:

I feel like that we do not have a list of cm commands that we test and that repeated fixing in some code has sideffects on others so we always end up with some bug as we do not do an exhaustive test  oliver can think about some tests for resevation from the commandline

I suggest we first collect a couple of commands tha we wantt o test and than develop some way of verifying iv the test works 

here my initial list

# HELP TESTS
cm help
cm help cloud
cm help flavor
cm help init
cm help list
cm help rain
cm help reservation
cm help storm
cm help vm
cm help defaults
cm help image
cm help inventory
cm help metric
cm help register
cm help security_group (this one has wrrnng name and I suggest we replace underscore with space)
cm help security

cm help user
cm help keys
 
# cloud commands
cm cloud list
cm cloud list —column=active,label,host
cm cloud list —column=all
cm cloud list all
$CLOUD = india_openstack_havana
cm cloud info $CLOUD



bug: the command cm cloud set name is unclear

bug the command cloud set NAME is unclear, is this the setting of the default cloud, if so should default be mentioned in the text

cloud on sierra_???
cloud off sierra_???
cloud remove sierra_???
cloud add sierra_???
cloud on sierra_???

do something useful here

# flavor comamnd

bug: use capital letters by in DOCOPT e.g. instead of cm_cloud use CLOUD to be compatible with other commands.
check all commands and use capital letters instaet of <> notation

bug: when i say 

cm flavor india_openstack_grizzly

(non existing cloud) it tries to authenticate with all clouds instead of just returning quickly an error. 
I assume its not necessary to autheticate to all clouds firs, but just do it when we call the appropriate cloud

bug: cm flavor —column=label,id

does not exist (low priority)

bug cm flavor all 

does not exist (low priority)


bug:

we used to have a —select option in the old cloudmesh code that when you for example say

cm flavors —select

looks up the name of the default cloud and than issues an ascii menu wheer you can chose a number and that flavor is going to be taked as the new default falvor for that cloud.

this should also apply for the cloud, and images commands

cm cloud —select
cm images —select

i actually think we should not use —select but inseat ust say 

cm flavor select

we also used to have an abbreviation for this with 

cm flavor ?

bug: we miss a comaand

cm list projects

cm list prooject NAME

# VM COMMANDS

vm create
vm create —label=silly

bug: we miss a command

vm last

that prints out info for the vm we started last

vm last -n=2

this is like previoys, but second last vm

bug:  we miss a command

vm history

listing the vms we previously submitted including their state

vm history —state

this is similar to 

vm list, but list does not specify the history

so we may want to also have a command 

vm list —history=ascending

sorting the list by the history in newest vm first

bug we do not have

vm create —label=? —image=? —cloud=?

same as 

vm create ?

which pops up various ascii menues for selecting things

vm create —label=somelabel —image=somerealimage —flavor=some real flavor —cloud=india_….
vm create —label=somelabel —image=somerealimage —flavor=some real flavor 
vm create —label=somelabel —image=somerealimage
vm create —label=somelabel —flavor=some real flavor 

bug:
vm delete 
which deletes tha last vm is not possibel right now due to lack of history

vm delete LABEL

# delete all vms on a cloud
vm delete CLOUD

bug DOCOPTS: repplace <> with capital letters

# defaults

bug:

cm defaults does not at all work. The defaults are actaully in mongo db 

we may want to add

cm deafult load mydefaulst.yaml 

that loads the defaults frm a yaml file and puts them into mongo

as this does not at all start i can not think about tests right now

# invetory

cm inventory

bug : looks like we have no inventory command implemented

# metric

Hyungro will develop a list of command shell around metric that seem useful for testing

# cm register

bug:
we will need to discuss if this command should be put into cloud

e.g. 

cm cloud register NAME


cm cloud activate NAME

# security group

bug:

command should be

cm security group
 
but i am not sure about that

we need some tests
BUG docopts capitalize
BUG add not implemented
BUG delete not implemented
BUG cm security group ? not implemented
BUG cm security group select not implemented
BUG cm_cloud change to CLOUD

# devise various test for keys (Mark)

# devise various tests for user (Fugang)

bug: cm should be able to be started without the server running, it shoudl however print a warning.

bug: if one of the clouds fails whn you say

cm flavor
cm image
or 
cm list image
cm list falvors

=======
TODO
====

help
----

cloud
-----

list
----

- [cm image] bug: cm image prints superhuge table making it impossible to display nicely

vm
--

defaults
--------

metrics
-------

