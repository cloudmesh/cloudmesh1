# Generate the classes for Users and Projects depending on the
# contents of the users and projects YAML file

import yaml
from cloudmesh_install import config_file

class_fields = "\t"


def build_field(item):
    for k, v in item.items():
        field_entry = k
        field_type = ""
        required = ""
        default_value = ""
        if isinstance(v, dict):
            for key, value in v.items():
                if key in ['required', 'type']:
                    if key == 'required':
                        required = key+"="+str(value)
                    elif key == 'type':
                        if value in ['text', 'textarea', 'dropdown']:
                            field_type = "StringField"
                        if value == 'checkbox':
                            field_type = "StringField"
                            default_value = "no"
                        elif value == 'email':
                            field_type = "EmailField"
        if default_value and required:
            field_entry = field_entry+" = "+field_type+"("+required+", default="+default_value+")"
        elif default_value and not required:
            field_entry = field_entry+" = "+field_type+"(default="+default_value+")"
        else:
            field_entry = field_entry+" = "+field_type+"("+required+")"
        return field_entry


def traverse_data(datum):
    global class_fields
    for k, v in datum.items():
        if isinstance(v, dict):
            traverse_data(v)
        else:
            if k == 'fields':
                for item in v:
                    entry = build_field(item)
                    class_fields = class_fields+entry+"\n\t"
    return class_fields


filename = config_file("/cloudmesh_user_intf.yaml")
data = yaml.load(open(filename))
fields = traverse_data(data)
print fields
