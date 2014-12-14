from __future__ import print_function
import datetime
import time
from mongoengine import Document
from mongoengine import *
from mongoengine import fields
import mongoengine

duration_in_weeks = 24


def order(mongo_class, exclude=None, include=None, custom=None, kind=None):
    class_fields = list(mongo_class.__dict__["_fields_ordered"])
    if kind in ['required', 'optional']:
        required = [
            k for k, v in mongo_class._fields.iteritems() if v.required]
        fields = class_fields
        optional = []
        for key in class_fields:
            if key not in required:
                fields.remove(key)
                optional.append(key)

        return (fields, optional)
    elif kind == "all":
        fields = class_fields
    else:
        if include is not None:
            fields = include
            for key in fields:
                if not key in class_fields:
                    print("Error: {0} not in fields".format(class_fields))
        else:
            fields = class_fields

        if exclude is not None:
            for key in exclude:
                fields.remove(key)

    return fields


def html_input_type(object, field):
    map = {mongoengine.fields.StringField: 'text'}
    # checkbox
    # textarea
    kind = type(object._fields[field])
    try:
        html_type = map[kind]
    except Exception, e:
        print("ERROR: {0} not supported".format(kind))
    return html_type


def wtf_type(object, field):
    return True


def make_form_list(object, fields, title="Form", format="p", capital=True):
    print(title)

    if format == "p":
        line_start = "<p>"
        line_end = "</p>"
        field_start = ""
        field_end = ""
    elif format == "table":
        line_start = "<tr>"
        line_end = "</tr>"
        field_start = "<td>"
        field_end = "</td>"

    labels = {}
    for label in fields:
        if capital:
            labels[label] = label.capitalize()
        else:
            labels[label] = label

    form = ""
    for key in fields:
        kind = html_input_type(object, key)
        form += '''
            {line_start}
                {field_start} <b>{label}</b> {field_end}
                {field_start} <input name="{key}" type="{input_type}"> {field_end}
            {line_end}'''.format(line_start=line_start,
                                 line_end=line_end,
                                 field_start=field_start,
                                 field_end=field_end,
                                 key=key,
                                 label=labels[key],
                                 input_type=kind)
    return form


class CloudmeshObject(Document):

    '''
    An Object for managing users and projects that includes default methods for
    activation, creation and modification dates.

    In future we will have a modification trace record here also. Arbitrary
    attributes can be added and modified with the set_attribute method
    '''

    active = BooleanField(default=False)
    date_modified = DateTimeField(default=datetime.datetime.now)
    date_created = DateTimeField()
    date_approved = None
    date_deactivated = DateTimeField()

    meta = {'allow_inheritance': True}

    def set_attribute(self, attribute, value):
        '''
        sets the attribute to the given value

        :param attribute: the attribute name
        :type attribute: String
        :param value: the value
        :type value: String
        '''
        self._data[attribute] = value

    def set_from_dict(self, d):
        '''
        sets a number of attributes contained within a key, value dict

        :param d:
        :type d:
        '''
        for key in d:
            self.set_attribute(key, d[key])

    def fields(self, kind=None):
        '''
        lists the attributes. One can select optional, required and all attributes

        :param kind: optional, required, all
        :type kind: String
        '''
        if kind is None or kind in ["all"]:
            return [k for k, v in self._fields.iteritems()]
        elif kind in ["optional"]:
            return [k for k, v in self._fields.iteritems() if not v.required]
        elif kind in ["required"]:
            return [k for k, v in self._fields.iteritems() if v.required]

    def activate(self, state=True):
        '''
        activates the object

        :param state: the state. True if active
        :type state: Boolean
        '''
        """activates a user"""
        self.active = state

    def deactivate(self):
        '''
        deactivates an object.
        '''
        self.activate(state=False)

    def set_date_deactivate(self, weeks=duration_in_weeks):
        '''
        deactivates the object after some duration specified as parameter.

        TODO: use readable times ... not just weeks

        :param weeks: number of weeks
        :type weeks: integer
        '''
        self.date_deactivate = datetime.datetime.now(
        ) + datetime.timedelta(weeks=weeks)
        # self.activate()
        return self.date_deactivate

    def save(self, *args, **kwargs):
        '''
        saves the object to the database
        '''
        if not self.date_created:
            self.date_created = datetime.datetime.now()
        self.date_modified = datetime.datetime.now()
        return super(CloudmeshObject, self).save(*args, **kwargs)
