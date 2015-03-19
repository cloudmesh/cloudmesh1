from os import listdir
from os.path import isfile, join
from flask import Blueprint
import flask
from cloudmesh_base.logger import LOGGER

flatpages_module = Blueprint('flatpages_module', __name__)

log = LOGGER(__file__)

pages_files = [f.replace(".md", "")
               for f in listdir("/static/pages") if isfile(join("/static/pages", f))]

sidebar_flatpages = []
for page in pages_files:
    sidebar_flatpages.append(
        {"url": "/static/" + page + "/", "name": page.capitalize()})

flask.Flask.app_ctx_globals_class.sidebar_flatpages = sidebar_flatpages

log.info(
    "{0}".format(str(flask.Flask.app_ctx_globals_class.sidebar_flatpages)))
