from django.conf.urls import patterns, include, url
from entity_management import EditProcess, CreateProcess

urlpatterns = patterns('',
    url(r'^process/create/$', CreateProcess.as_view(), name="create_process"),
    url(r'^process/(?P<name>[0-9a-zA-Z@\-]+)/edit', EditProcess.as_view(), name="edit_process"),
)

urlpatterns += patterns('dashboard.views',

    url(r'^(?P<type>[a-z]+)/(?P<name>[0-9a-zA-Z@\-]+)/$', 'entity_details', name="entity_details"),
    url(r'^$', 'search_entity'),
)

