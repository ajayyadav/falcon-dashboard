from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic.base import View
from api.views import get_feeds_status, get_feed_summary, get_process_summary


class Index(View):

    def get(self, request, template_name = "monitoring/monitoring_index.html"):
        current_app = 'monitoring'
        pipelines = ["CAS-dwh-pipeline","Yoda-daily-pipeline","Local-DC-Pipeline","DWH-pipeline","RR-NOB-pipeline","User-Pipeline"]
        return render(request, template_name, locals())


    def post(self, request):
        #find pipeline name from the request and redirect it to 
        template_name="monitoring/pipeline_summary.html"
        return HttpResponseRedirect(reverse('pipeline_summary', kwargs={'pipeline_name': 'CAS'}))



def pipeline_summary(request, pipeline_name, template_name="monitoring/pipeline_summary.html"):
    current_app = 'monitoring'    
    summary = {

    'global':{'feeds': (
        ('CAS-global-dwh-minutely',23,48,0,1,2),
        ('CAS-global-dwh-hourly',23,48,0,1,2),
        ('CAS-global-dwh-daily',23,48,0,1,2),
        ('CAS-global-dwh-weekly',23,48,0,1,2),
        ),

    'processes': (
        ('CAS-global-dwh-summary-generator',23,48,0,1,2),
        ('CAS-global-daily-generator',23,48,0,1,2),
        ('CAS-global-weekly-generator',23,48,0,1,2),
        ('CAS-global-monthly-generator',23,48,0,1,2),  
        )
    },

    'hkg1':{'feeds': (
        ('CAS-local-dwh-minutely',23,48,0,1,2),
        ('CAS-local-dwh-hourly',23,48,0,1,2),
        ('CAS-local-dwh-daily',23,48,0,1,2),
        ('CAS-local-dwh-weekly',23,48,0,1,2),
        ),

    'processes': (
        ('CAS-local-dwh-summary-generator',23,48,0,1,2),
        ('CAS-local-rmc-daily-generator',23,48,0,1,2),
        ('CAS-local-dwh-weekly-generator',23,48,0,1,2),
        ('CAS-local-dwh-monthly-generator',23,48,0,1,2),  
        )
    }

    }    
    return render(request, template_name, locals())


def process_summary(request, process_name, template_name="monitoring/process_summary.html"):
    current_app='monitoring'
    status = get_process_summary(process_name)
    return render(request, template_name, locals())    

def feeds_dashboard(request, template_name="monitoring/monitor_feed.html"):
    status = get_feeds_status()
    current_app = 'monitoring'
    return render(request, template_name, locals())
    

def feed_summary(request, feed_name, template_name='monitoring/feed_summary.html'):
    current_tab = 'feed-sla-list'
    current_app = 'monitoring'
    status = get_feed_summary()
    return render(request, template_name, locals())


def feed_sla_graph(request, feed_name, template_name="monitoring/feed_sla_graph.html"):
    current_app = 'monitoring'
    current_tab = 'feed-sla-graph'
    return render(request, template_name, locals())

    
def feed_space_usage_graph(request, feed_name, template_name="monitoring/feed_space_usage_graph.html"):
    current_app = 'monitoring'
    current_tab = 'feed-disk-usage'
    return render(request, template_name, locals())


def entity_summary(request, template_name=""):
    pass

def instance_dependency_graph(request, template_name=""):
    pass