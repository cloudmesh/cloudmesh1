from os import listdir
from os.path import isfile, join
from flask import Blueprint
import flask
from cloudmesh.util.logger import LOGGER

flatpages_module = Blueprint('flatpages_module', __name__)

log = LOGGER(__file__)

pages_files = [f.replace(".md", "")
               for f in listdir("./pages") if isfile(join("./pages", f))]

sidebar_flatpages = []
for page in pages_files:
    sidebar_flatpages.append(
        {"url": "/" + page + "/", "name": page.capitalize()})

flask.Flask.app_ctx_globals_class.sidebar_flatpages = sidebar_flatpages

log.info(
    "{0}".format(str(flask.Flask.app_ctx_globals_class.sidebar_flatpages)))
