from sh import gmkproject
from sh import gchproject
from sh import gchuser
#

class AccountingBaseClass:

    #all methods return some kind of id if possible or useful or the object
    
    def  add_project(self, name, description):
        print "not yet implemented"
        pass

    def deactivate_project(self, name):
        print "not yet implemented"
        pass

    def add_user(self, firstname, lastname, e-mail, phone):
        print "not yet implemented"
        pass

    def modify_user(self, userid, firstname, lastname, e-mail, phone):
        print "not yet implemented"
        pass

    def add_user_to_project (self, project, userid):
        print "not yet implemented"
        pass

    def deactivate_user_from_project (self, project, userid):
        print "not yet implemented"
        pass

    def activate_user_from_project (self, project, userid):
        print "not yet implemented"
        pass

class GoldAccounting(AccountingBaseClass):

    def project_usage (self, project)
        statement = gstatement("-p", project)
        return statement
    # what does summarize do
    # needs to return dict    

    def user_usage(self, userid):
        statement = gstatement("-u", userid)
        return statement
    # needs to return dict
        
    def projects(self, userid):
        list = glusers("--show", "Projects", userid, "-l", "--quiet")
        return list
    # what does --raw do?
        # bug this should be returned as a list while removing \n and
        # putting it in a list instead of a string
        
    def users(self):
        list = glusers("--show Name","--quiet")
        return list
        # bug this should be returned as a list while removing \n and
        # putting it in a list instead of a string
        
    def default_project(self, userid, project):
        # can be done with gchgsuser
        pass

    def modify_user(self, userid, email=None, phone=None,
                    firstname=None, lastname=None):
        # needs to check if common name is unique, if its not we may
        # want to add numbers
        if firstname != None or lastname != None:
            gchguser("-n", "%s %s" % (firstname, lastname))
        if email != None:
            gchguser("-E", email)
        if phone != None:
            gchguser("-F", phone)

    def  add_project(self, name):
        gmkproject("-d",description,"-p", name)

    def add_user_to_projects(self, project, userid):
        gchproject("-addUsers", username, project)

    def deactivate_project(self, name):
        gchproject("-I", name)

    def deactivate_user_from_project (self, project, userid):
        gchproject("--deactUsers", userid)

    def activate_user_from_project (self, project, userid):
        gchproject("--actUsers", userid)

