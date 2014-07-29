from django.conf.urls import patterns, include, url
from entity_management import UpdateProcess, CreateProcess, UpdateFeed, CreateFeed, UpdateCluster, CreateCluster

urlpatterns = patterns('',
    url(r'^process/create/$', CreateProcess.as_view(), name="create_process"),
    url(r'^feed/create/$',  CreateFeed.as_view(), name="create_feed"),
    url(r'^cluster/create/$', CreateCluster.as_view(), name="create_cluster"),

    url(r'^process/(?P<name>[0-9a-zA-Z@\-]+)/edit', UpdateProcess.as_view(), name="edit_process"),
    url(r'^feed/(?P<name>[0-9a-zA-Z@\-]+)/edit', UpdateFeed.as_view(), name="edit_feed"),
    url(r'^cluster/(?P<name>[0-9a-zA-Z@\-]+)/edit', UpdateCluster.as_view(), name="edit_cluster"),
)

urlpatterns += patterns('dashboard.views',

    url(r'^(?P<type>[a-z]+)/(?P<name>[0-9a-zA-Z@\-]+)/$', 'entity_details', name="entity_details"),
    url(r'^$', 'search_entity'),
)

