from __future__ import print_function


class cm_projects():

    cm_kind = "fg_project"
    project_url_basename = "https://portal.futuregrid.org/projects/"

    def __init__(self):
        raise NotImplementedError()

    def update(self):
        """retrieves the information from the portal into mongo"""
        raise NotImplementedError()

    def number(self, identifier):
        """
        returns the number of a probect. Input can be.
        Assume number is 82

        82, fg82, fg-82, FG82, FG-82
        fg can aslo be uppercase
        """
        raise NotImplementedError()
        _id = itentifier.lower()
        if _id.startswith("fg-"):
            # fg-82
            number = identifier.replace("fg-", "")
        elif _id.startswith("fg"):
            # fg82
            number = identifier.replace("fg", "")
        else:
            # we just assume a number
            number = _id
        return str(number)

    def url(self, identifier):
        return project_url_basename + id(identifier)

    def info(self, identifier, unavailable="not available"):
        """
        returns a dict with the information about the project.
        This includes
           title
           description

            other information may be added in future.

            If no information is available it will return
            description = "not available"
            title = "not available"
            the messgae can be set with unavailable = "msg"
        """
        number = id(identifier)
        raise NotImplementedError()

    def add(self, identifier, **kwargs):
        """
        adds the named attributes to the mongo db for the given project
        """
        raise NotImplementedError()
