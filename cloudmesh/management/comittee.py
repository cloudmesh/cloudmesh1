from mongoengine import *
from datetime import datetime
from project import Project, Projects
from user import User, Users

port = 27777
db_name = 'project'

users = Users()
projects = Projects()


def IMPLEMENT():
    print "IMPLEMENT ME"

DEFAULT_REVIEWERS = ('gregvon', 'gregvon1')

STATUS = ('pending', 'approved', 'disapproved')

CHOICES = ('Yes', 'No')


class Committee(Document):
    status = StringField(choices=STATUS)
    projects = ListField(StringField())
    reviewers = ListField(ReferenceField(User), default=[])
    reviews = StringField()
    #--------------------------------------------------------------------
    #	Default value showing if this is the first time the project is being applied for or not
    #--------------------------------------------------------------------
    default = StringField(choices=CHOICES, default='Yes')
    message = StringField()

    def __str__(self):
        return "{0} {1} {2} {3}".format(self.status, self.reviewers)

    def set_committee(self):
        pass

    def get_project(self, title):
        """This function wold be deleted later after we have been able
        call this class from the project class, hence this is a sample"""
        _project = projects.find_by_title("Django")

    def get_reviewer(self, user_name):
        """This function adds reviewers to the project committee. It first 
        checks if the default attribute is 'Yes' or 'No', if 'Yes' it adds 
        the default reviewers and if 'No' it does otherwise"""
        if self.default == 'Yes':
            for _username in DEFAULT_REVIEWERS:
                default_reviewer = users.find_user(_username)
                self.add_reviewers(default_reviewer)
            self.default == 'No'
        elif self.default == 'No':
            _reviewer = users.find_user(user_name)
            self.add_reviewers(_reviewer)

    def add_reviewers(self, user):
        """This function adds users to the reviewers list"""
        self.reviewers.append(user)

    def set_review(self, project, user, msg):
        """by set_review, do you mean to state whether
        approved or not and what type of message am I meant to 
        pass into this function"""

        IMPLEMENT()

    def delete_reviewer(self, project, user):
        """This function accepts a user and removes the user 
        from the committee list"""
        self.reviewers.remove(user)

    def notify_project_management(self, project, msg):
        IMPLEMENT()

    def notify_project_members(self, project, msg):
        IMPLEMENT()

    def notify_project_alumni(self, project, msg):
        IMPLEMENT()

    def notify_reviewers(self, project, msg):
        IMPLEMENT()

    def notify_all_reviewers(self, msg):
        IMPLEMENT()

    def enable(self, bool):
        """enables or disables reviews, useful for maintenance"""
        IMPLEMENT()

    def pending_projects(self):
        return self.get_by_status("pending")

    def approved_projects(self):
        return self.get_by_status("approved")

    def disproved_projects(self):
        return self.get_by_status("disproved")

    def completed_projects(self):
        return self.get_by_status("completed")

    def get_by_status(self,  status):
        if status in STATUS:
            IMPLEMENT()
        else:
            print "ERROR: wrong status", status
            return None


def main():

    comittee = Committee()
    print comittee.default
    comittee.get_reviewer("fugang")
    print comittee.reviewers

    projects = Projects()

    for project in Project.objects():
        print project


if __name__ == "__main__":
    main()
