from django.shortcuts import render
from api.views import e_search, e_definition, e_instances, e_dependency

# Not sure if they are needed
# get names for all feeds - this is for autocomplete - cache it 
# needed for autocomplete in case of editing/updating a process


# get names for all process - this is for autocomplete - cache it
# get names for all clusters - this is for autocomplete - cache it

#TODO: check if different functions are needed for feed,process and cluster ????


# search for the entity containing this text (case insensitive)
def search_entity(request, template_name='dashboard/search.html'):
    type = request.GET.get('type')
    query = request.GET.get('name')
    # dictionary containing entity name and entity type
    if type and query:
        results =  e_search(type, query)
    else:
        results = []
    return render(request, template_name, locals())


def entity_details(request, type, name, template_name='dashboard/entity_details.html'):
    """Show details of the entity with given type and name"""
    entity_definition = e_definition(type, name)
    dependencies = e_dependency(type,name)
    instances = e_instances(type,name) # return last 5 instances of this process
    return render(request, template_name, locals() )


def edit_process(request, name):
    pass

def edit_process(request, name):
    pass

def edit_process(request, name):
    pass


def edit_entity(request, type, name):

    if type == 'process':
        return edit_process(request, name)
    elif type == 'feed':
        return edit_feed(request, name)
    else:
        return edit_cluster(request, name)