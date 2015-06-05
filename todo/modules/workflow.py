from cloudmesh_base.Shell import Shell
from flask import Blueprint
from flask import render_template, redirect, flash
from datetime import datetime
from flask.ext.wtf import Form
from wtforms import TextField, SelectField, TextAreaField
from cloudmesh.old_inventory.inventory import Inventory
from hostlist import expand_hostlist
from cloudmesh.provisioner.provisioner import *
from cloudmesh.old_inventory.inventory import PROVISIONING_CHOICES
from cloudmesh.provisioner.queue.celery import celery
from cloudmesh.provisioner.queue.tasks import provision
from cloudmesh.config.cm_config import cm_config_server
from pprint import pprint
from cloudmesh.util.util import path_expand
from cloudmesh.util.util import cond_decorator
from cloudmesh.inventory import Inventory

from cloudmesh.util.webutil import decode_source
from flask import Blueprint, request, make_response, render_template
from flask.ext.login import login_required
import cloudmesh

from flask.ext.principal import Permission, RoleNeed
from cloudmesh.util.logger import LOGGER

log = LOGGER(__file__)

workflow_module = Blueprint('workflow_module', __name__)

admin_permission = Permission(RoleNeed('admin'))

diagram_format = "svg"


class ProvisionWorkflowForm(Form):
    # print
    # "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++",Form
    filename = "abc"

    dir = path_expand(
        cm_config_server().get("cloudmesh.server.workflows.path"))

    # not so nice cludge, ask for location of statcic instead

    web_pwd = Shell.pwd().strip()
    basename = "/static/{0}/{1}".format(dir, filename)

    print "BBBB", basename
    try:
        with open("{2}/{0}.{1}".format(basename, "diag", web_pwd), "r") as f:
            data = f.readlines()[1:-1]
            default = "".join(data)
    except:
        print "Error: diagram not found"
        default = ""
    default = default.split("//graph")
    filename = TextField("Filename", default=filename)
    # properties = TextAreaField("Workflow", default=default[0])
    # workflow = TextAreaField("Workflow", default=default[1])
    properties = TextAreaField("Workflow", default="fake")
    workflow = TextAreaField("Workflow", default="fake")
    # print workflow


# ============================================================
# ROUTE: workflows
# ============================================================


@workflow_module.route('/workflows/<filename>')
@login_required
@admin_permission.require(http_exception=403)
def retrieve_files(filename):
    """    Retrieve files that have been uploaded    """
    return send_from_directory('/tmp/workflows', filename)


@workflow_module.route("/provision/workflow/", methods=("GET", "POST"))
@login_required
@admin_permission.require(http_exception=403)
def display_provision_workflow_form():

    form = ProvisionWorkflowForm(csrf=False)

    dir = path_expand(
        cm_config_server().get("cloudmesh.server.workflows.path"))

    filename = "abc"

    web_pwd = Shell.pwd().strip()
    print "PWD", web_pwd
    basename = "/static/{0}/{1}".format(dir, filename,)
    # if form.validate_on_submit():

    #    print "SKIP"
    try:
        with open("{2}/{0}.{1}".format(basename, "diag", web_pwd), "w") as f:
            # print "########################################################################################"
            # print "aaaaaa"+form.workflow.data+"bbb"
            f.write("blockdiag {\n")
            if form.workflow.data == "":
                form.work.data = f.work.default
            if form.properties.data == "":
                form.properties.data = form.properties.default
            f.write(form.properties.data)
            f.write("//graph\n")
            f.write(form.workflow.data)
            f.write("\n}")

            # print
            # "########################################################################################"
            print form.workflow
    except:
        print "file does not exists"
    print "{0}.{1}".format(basename, diagram_format)

    print "OOOO", basename
    Shell.blockdiag("--ignore-pil", "-Tsvg",
              "-o", "{2}/{0}.{1}".format(basename, diagram_format, web_pwd),
              "{2}/{0}.{1}".format(basename, "diag", web_pwd))
    # Shell.blockdiag("-Tpng",
    #          "-o", "." + dir + filename + ".png",
    #          "." + dir + filename + ".diag")

    # else:
    #    flash("Wrong submission")
    inventory.refresh()
    return render_template("provision_workflow.html",
                           workflow=form.workflow.data,
                           form=form,
                           pwd=pwd,
                           diagram="{0}.{1}".format(basename, diagram_format),
                           inventory=inventory)


"""

 this is not used
 
@workflow_module.route('/workflow/')
@login_required
@admin_permission.require(http_exception=403)
def display_workflow():

    print "DISPALY WORKFLOW"
    kwargs = {}

    # url = get_redirect_url('workflow', request)
    # if url:
    #    return redirect(url)

    source = request.args.get('src')
    print "SOURCE", source, kwargs

    if source:
        compression = request.args.get('compression')
        kwargs['diagram'] = decode_source(source, 'base64', compression)

    body = render_template('workflow.html', **kwargs)
    response = make_response(body)
    response.headers['Content-Type'] = 'application/xhtml+xml'
    return response
    # return body

"""
