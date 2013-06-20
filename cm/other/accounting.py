#! /usr/bin/python                                                                                                                                                                                     

from sh import ls

class gold:
    def info(self):

        out = ls("-lisA")

        print out


g = gold()

g.info()


Example 3-1. Let’s add the users amy, bob and dave.
$ gmkuser -n "Wilkes, Amy" -E "amy@western.edu" amy
         Successfully created 1 User
$ gmkuser -n "Smith, Robert F." -E "bob@western.edu" bob
         Successfully created 1 User
$ gmkuser -n "Miller, David" -E "dave@western.edu" dave
         Successfully created 1 User
$ glsuser

$ gmkmachine -d "Linux Cluster" colony
         Successfully created 1 Machine
$ gmkmachine -d "IBM SP2" blue
         Successfully created 1 Machine
$ glsmachine

$ gmkproject -d "Biology Department" biology
         Successfully created 1 Project
         Auto-generated Account 1
$ gmkproject -d "Chemistry Department" chemistry
         Successfully created 1 Project
         Auto-generated Account 2
$ glsproject


$ gchproject --addUsers amy,bob biology
         Successfully created 1 ProjectUser
         Successfully created 1 ProjectUser
$ gchproject --addUsers amy,bob,dave chemistry
         Successfully created 1 ProjectUser
         Successfully created 1 ProjectUser
         Successfully created 1 ProjectUser
$ glsproject
         Name      Active Users        Machines Description
         --------- ------ ------------ -------- --------------------
         biology   True   amy,bob               Biology Department
         chemistry True   amy,dave,bob          Chemistry Department



$ gdeposit -s 2005-01-01 -e 2006-01-01 -z 360000000 -p biology
         Successfully deposited 360000000 credits into account 1
$ gdeposit -s 2005-01-01 -e 2006-01-01 -z 360000000 -p chemistry
         Successfully deposited 360000000 credits into account 2
Let’s examine the allocations we just created
$ glsalloc


$ gbalance -u amy
         Id Name      Amount    Reserved Balance   CreditLimit Available
         -- --------- --------- -------- --------- ----------- ---------
         1  biology   360000000 0        360000000 0           360000000
         2  chemistry 360000000 0        360000000 0           360000000
Example 3-7. You may just want the total balance for a certain project and machine
$ gbalance -u amy -p chemistry -m colony --total

$ gcharge -J PBS.1234.0 -u amy -p chemistry -m colony -P 16 -t 1234 -X WallDuration=1234

