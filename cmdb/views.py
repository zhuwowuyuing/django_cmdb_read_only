import logging

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context, Template, RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404

from misc.cmdb_lib import get_parent_paths, get_correct_class, \
    get_schema_for_ci, prefix_slash
from cmdb.models import *
from cmdb.forms import *

def view_ci(request, ci_path):

    as_json = request.POST.get('as_json')
    ci_path = prefix_slash(ci_path) 
    # Is user allowed to view this CI?
    schema = get_schema_for_ci(ci_path=ci_path)
    try:
        ci = eval('''%s.objects.get(path='%s')''' % (schema.class_name, ci_path))
    except:
        ci = False

    if ci:
        return render_to_response(schema.view_template, locals(), context_instance=RequestContext(request))
    else:
        handle_404_error(ci_path)

def add_ci(request):

    if request.method == 'GET':
        ci_path = request.GET.get('path')
        logging.debug('''Adding CI under %s''' % ci_path)
        schema = get_schema_for_ci(ci_path=ci_path)
        form = eval(schema.form_name)()
        return render_to_response(schema.add_template, locals(), context_instance=RequestContext(request))


    if request.method == 'POST':
        # Add object
        pass


@login_required
def decommission_ci(request, *args, **kwargs):
    if not kwargs.has_key('ci'):
        ci = ConfigurationItem.objects.get(path=kwargs['ci_path'])
    else:
        ci = kwargs['ci']
        logging.debug("class of object is %s" % ci.__class__)

    ci_to_decom = get_correct_class(ci=ci)
    ci_to_decom.active = False
    ci_to_decom.save()
    logging.debug('''Decommissioned CI: %s''' % ci.path)

def handle_404_error(ci_path):
    raise Http404()

    
    
