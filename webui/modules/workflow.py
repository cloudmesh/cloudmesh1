# -*- coding: utf-8 -*-
from cloudmesh.util.webutil import decode_source, get_redirect_url, simplejson
from flask import Blueprint, redirect, request, make_response, render_template

workflow_module = Blueprint('workflow_module', __name__)


@workflow_module.route('/')
def display_workflow():

    print "DISPALY WORKFLOW"
    kwargs = {}

    #url = get_redirect_url('workflow', request)
    #if url:
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
    #return body