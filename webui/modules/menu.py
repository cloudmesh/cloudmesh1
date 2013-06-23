from flask import Blueprint

menu_api = Blueprint('menu_api', __name__)

######################################################################
# ACTIVATE STRUCTURE
######################################################################


list_of_sidebar_pages = {
    'home': {"url" : "/", "name" : "Home", "active" : ""},
    'inventory': {"url" : "/inventory", "name" : "Inventory", "active" : ""},
    'inventory_images': {"url" : "/inventory/images", "name" : "Inventory Images", "active" : ""},
    'table': {"url" : "/table", "name" : "VMs", "active" : ""},
    'images': {"url" : "/images", "name" : "Images", "active" : ""},
    'metric': {"url" : "/metric/main", "name" : "Metric", "active" : ""},
    'projects': {"url" : "/projects", "name" : "Projects", "active" : ""},
    'flavors': {"url" : "/flavors", "name" : "Flavors", "active" : ""},
    'profile': {"url" : "/profile", "name" : "Profile", "active" : ""},
    'keys': {"url" : "/keys", "name" : "Keys", "active" : ""},
    }

list_of_flatpages = {}
for page in pages_files:
    list_of_flatpages[page] = {page: {"url": "/pages/" + page, "name": page.capitalize(), "active": ""}}

    #pp.pprint (list_of_sidebar_pages)
    #pp.pprint (list_of_flatpages)


@menu_app.context_processor
def inject_sidebar():
    return dict(sidebar_pages=list_of_sidebar_pages)

@menu_app.context_processor
def inject_flatpages():
    return dict(flat_pages=list_of_flatpages)

def make_active(name):
    for page in list_of_sidebar_pages:
        list_of_sidebar_pages[page]["active"] = ""
    for page in list_of_flatpages:
        list_of_flatpages[page]["active"] = ""
    try:
        list_of_sidebar_pages[name]["active"] = 'active'
    except:
        pass
    try:
        list_of_flatpages[name]["active"] = 'active'
    except:
        pass

