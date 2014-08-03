from django.conf.urls import patterns, include, url
from views import Index

urlpatterns = patterns('monitoring.views',

	#feed mon related links
    url(r'^feeds/$', 'feeds_dashboard', name="feeds_dashboard"),
    url(r'^feeds/(?P<feed_name>[a-zA-Z0-9\-]+)/$', 'feed_summary', name="feed_summary"),
    url(r'^feeds/(?P<feed_name>[a-zA-Z0-9\-]+)/sla/$', 'feed_sla_graph', name="feed_sla_graph"),
    url(r'^feeds/(?P<feed_name>[a-zA-Z0-9\-]+)/size/$', 'feed_space_usage_graph', name="feed_space_usage_graph"),

    #process summary
    url(r'^process/(?P<process_name>[a-zA-Z0-9\-]+)/$', 'process_summary', name="process_summary"),
    #pipeline summary
    url(r'^pipeline/(?P<pipeline_name>[a-zA-Z0-9\-]+)/$', 'pipeline_summary', name="pipeline_summary"),
)

urlpatterns += patterns('',
	url(r'^$', Index.as_view(), name="monitoring_index"),
)

urlpatterns += patterns('monitoring.views',
	url(r'^entity/(?P<entity_name>[0-9a-zA-Z@\-]+)/(?P<time_range>[\d]+)/', 'entity_summary', name='entity-summary' ), #pipeline/name of pipeline/1
    url(r'^entity/(?P<entity_name>[0-9a-zA-Z@\-]+)/(?P<time_range>[\d]+)/(?P<status>[\w]+)/', 'entity_summary', name='entity-summary' ), #pipeline/name of pipeline/1/failed
    url(r'^entity/(?P<instance_id>[0-9a-zA-Z\-]+)/', 'instance_dependency_graph', name='dependency-graph' ), #pipeline/name of pipeline/1
)
