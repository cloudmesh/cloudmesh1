from cloudmesh_base.Shell import Shell
from cloudmesh.accounting.AccountingBaseClass import AccountingBaseClass


class GoldAccounting(AccountingBaseClass):

    """The gold accounting implementation class"""

    def project_usage(self, project):
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
        list = glusers("--show Name", "--quiet")
        return list
        # bug this should be returned as a list while removing \n and
        # putting it in a list instead of a string

    def default_project(self, userid, project):
        # can be done with gchsuser
        pass

    def modify_user(self, userid, email=None, phone=None,
                    firstname=None, lastname=None):
        # needs to check if common name is unique, if its not we may
        # want to add numbers
        if firstname is not None or lastname is not None:
            gchuser("-n", "%s %s" % (firstname, lastname))
        if email is not None:
            gchuser("-E", email)
        if phone is not None:
            gchuser("-F", phone)

    def add_project(self, name, description):
        Shell.gmkproject("-d", description, "-p", name)

    def add_user_to_projects(self, project, userid):
        username = None  # transfer user id to username
        Shell.gchproject("-addUsers", username, project)

    def deactivate_project(self, name):
        Shell.gchproject("-I", name)

    def deactivate_user_from_project(self, project, userid):
        Shell.gchproject("--deactUsers", userid)

    def activate_user_from_project(self, project, userid):
        Shell.gchproject("--actUsers", userid)
