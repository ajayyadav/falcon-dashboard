from django.template.loader import get_template
from django.template import Context, Template
from django.shortcuts import render
from django.views.generic.base import View
from api.views import e_create_process

import xml.etree.ElementTree as ET


def parse_feed(xml):
    # you can replace both the following lines with: root = ET.fromstring(country_data_as_string)
    tree = ET.parse('/Users/ajay.yadav/feed.xml')
    root = tree.getroot()
    pass

def parse_cluster(feed):
    pass

def parse_process(feed):
    # parse name
    tree = ET.parse('/Users/ajay.yadav/process.xml')
    root = tree.getroot()
    dict = {}
    dict['name'] = root.attrib['name']

    #find cluster name, start and end for each cluster
    
    # input-feeds: name, alias, partition, isoptional, start and end
    #output-feeds: name, alias, instance
    #property: key value pair
    #workflow-name: wf-location

    pass




def create_process_context(request):
    d = request.POST.copy()

    # get all cluster inputs and add them into clusters
    clusters = []
    counter = 1
    while  True:
        try:
            cluster={}
            cluster['name'] = d['cluster-'+str(counter)]
            cluster['start'] = d['cluster-start-'+str(counter)].replace(' ','T') + 'Z'
            cluster['end'] = d['cluster-end-'+str(counter)].replace(' ','T') + 'Z'
            clusters.append(cluster)
            counter +=1
        except KeyError as e:
            counter = 1
            break
    d['clusters'] = clusters

    # get all feed inputs and add them into input_feeds
    input_feeds=[]
    while  True:
        try:
            feed = {}
            feed['name'] = d['input-feed-'+str(counter)]
            feed['start'] = d['input-feed-start-'+str(counter)].replace(' ','T') + 'Z'
            feed['end'] = d['input-feed-end-'+str(counter)].replace(' ','T') + 'Z'
            feed['alias'] = d['input-feed-alias-'+str(counter)]
            feed['partition'] = d.get('input-feed-partition-'+str(counter))
            feed['optional'] = True if d['input-feed-optional-'+str(counter)] == '1' else False
            input_feeds.append(feed)
            counter +=1
        except KeyError as e:
            counter = 1
            break
    d['input_feeds'] = input_feeds
    # get all feed outputs and add them into output_feeds
    output_feeds = []
    while  True:
        try:
            feed = {}
            feed['name'] = d['output-feed-'+str(counter)]
            feed['alias'] = d['output-feed-alias-'+str(counter)]
            feed['instance'] = d['output-feed-instance-'+str(counter)]
            output_feeds.append(feed)
            counter +=1
        except KeyError as e:
            counter = 1
            break
    d['output_feeds'] = output_feeds
    # get all properties and add them into properties
    properties=[]
    while  True:
        try:
            properties.append([ d['property-key-'+str(counter)], d['property-value-'+str(counter)] ] )
            counter +=1
        except KeyError as e:
            counter = 1
            break
    d['properties'] = properties
    print d
    return d
    
class EditProcess(View):
    template_name = 'dashboard/edit_process.html'
    def get(self, request, name):
        # <view logic>
        return render(request, self.template_name)

    def post(self, request, name):
        return render(request, self.template_name)


class CreateProcess(View):
    template_name = 'dashboard/create_process.html'
    xml_template = 'dashboard/process_definition.xml'

    def get(self, request):
        # <view logic>
        clusters=['hkg1', 'lhr1', 'ua2']
        feeds = ['CAS-local-dwh-hourly', 'CAS-dwh-daily']
        return render(request, self.template_name, locals())

    def post(self, request):
        # create the context dict for the template and generate the xml 
        cont = create_process_context(request)
        c = Context(cont)
        t =  get_template(self.xml_template)
        process_definition =t.render(c)
        # write the xml to file in api method
        e_create_process(process_definition)
        # generate success message and take to entity details page for that process
        return render(request, self.template_name)

