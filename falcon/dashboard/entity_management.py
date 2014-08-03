from django.template.loader import get_template
from django.template import Context, Template
from django.shortcuts import render
from django.views.generic.base import View
from api.views import e_create_process, get_process_definition, get_feeds_list, get_clusters_list
from api.views import get_workflows

import xml.etree.ElementTree as ET
import json

class CreateProcess(View):
    template_name = 'dashboard/create_process.html'
    xml_template = 'dashboard/process_definition.xml'

    def get(self, request):
        current_app='designer'
        clusters = get_clusters_list()
        feeds = get_feeds_list()
        workflows = get_workflows()
        return render(request, self.template_name, locals())

    def post(self, request):
        # create the context dict for the template and generate the xml 
        current_app='designer'
        cont = create_process_context(request)
        c = Context(cont)
        t =  get_template(self.xml_template)
        process_definition =t.render(c)
        # write the xml to file in api method
        e_create_process(process_definition)
        # generate success message and take to entity details page for that process
        return render(request, self.template_name)

class UpdateProcess(View):
    template_name = 'dashboard/edit_process.html'

    def get(self, request, name):
        # api: get definition of process with this name - json
        current_app='designer'
        process = get_process_definition(name)
        feeds = get_feeds_list()
        clusters = get_clusters_list()
        workflows = get_workflows()
        # import pdb; pdb.set_trace()
        #TODO: handle the case where name provided is incorrect
        return render(request, self.template_name, {'p':process,'feeds':feeds,'clusters':clusters,'workflows':workflows,'current_app':current_app})

    def post(self, request, name):
        current_app='designer'
        # api: update the process with name - should accept json
        # TODO: handle the errors case, highlight and show it to user
        # TODO: show disappearing success message and redirect to entity_details page
        return render(request, self.template_name, locals())

class CreateFeed(View):
    pass

class UpdateFeed(View):
    template_name = 'dashboard/edit_process.html'

    def get(self, request, name):
        # api: get definition of process with this name - json
        process = get_process_definition(name)
        current_app='designer'
        #TODO: handle the case where name provided is incorrect
        return render(request, self.template_name, locals())

    def post(self, request, name):
        # api: update the process with name - should accept json
        # TODO: handle the errors case, highlight and show it to user
        # TODO: show disappearing success message and redirect to entity_details page
        current_app='designer'
        return render(request, self.template_name,locals())

class CreateCluster(View):
    pass

class UpdateCluster(View):
    template_name = 'dashboard/edit_process.html'

    def get(self, request, name):
        current_app='designer'
        # api: get definition of process with this name - json
        process = get_process_definition(name)
        #TODO: handle the case where name provided is incorrect
        return render(request, self.template_name, {'process':process})

    def post(self, request, name):
        current_app='designer'
        # api: update the process with name - should accept json
        # TODO: handle the errors case, highlight and show it to user
        # TODO: show disappearing success message and redirect to entity_details page
        return render(request, self.template_name)

