from django.shortcuts import render

# Create your views here.
def e_search(type, name):
    resp = ["CAS-local-dwh-hourly-summary", "CAS-rmc-hourly"]
    return resp

def e_create_process(definition):
    with open('/tmp/process_definition.xml','w') as f:
        f.write(definition)
    pass
  

def e_definition(type, name):
    """Show details of the entity with given type and name"""
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
            <process name="SampleProcess" xmlns="uri:falcon:process:0.1">
              <clusters>
                <cluster name="primary-cluster">
                  <validity start="2012-04-03T06:00Z" end="2022-12-30T00:00Z"/>
                </cluster>
              </clusters>
              <parallel>1</parallel>
              <order>FIFO</order>
              <frequency>hours(1)</frequency>
              <timezone>UTC</timezone>
              <inputs>
                <input name="input" feed="SampleInput" start="yesterday(0,0)" end="today(-1,0)"/>
              </inputs>
              <outputs>
                <output name="output" feed="SampleOutput" instance="yesterday(0,0)"/>
              </outputs>
              <properties>
                <property name="queueName" value="default"/>
                <property name="ssh.host" value="localhost"/>
                <property name="fileTimestamp" value="{coord:formatTime(coord:nominalTime(), 'yyyy-MM-dd')}"/>
              </properties>
              <workflow engine="oozie" path="/examples/apps/aggregator"/>
              <retry policy="exp-backoff" delay="minutes(5)" attempts="3"/>
              <late-process policy="exp-backoff" delay="hours(1)">
                <late-input input="input" workflow-path="/projects/bootcamp/workflow/lateinput"/>
              </late-process>
            </process>"""


# get instances of a process/feed
def e_instances(type, name, start_time=None, end_time=None):
    # what are reasonable defaults?? - if no start or end time return last 5 instances
    return [
            {'time':'2014-07-16-10:00', 'status':'running', 'log_link':'', 'lineage_link':''},
            {'time':'2014-07-16-09:00', 'status':'failed', 'log_link':'', 'lineage_link':''},
            {'time':'2014-07-16-08:00', 'status':'succeeded', 'log_link':'', 'lineage_link':''},
            {'time':'2014-07-16-07:00', 'status':'succeesded', 'log_link':'', 'lineage_link':''},
        ]

# get logs for a process/feed
def entity_logs(request, type, name):
    # do logs for feeds make sense ??
    pass

# get lineage of an instance of process/feed
def entity_lineage(request, type, name):
    pass

def instance_lineage(request, type, name, instance_id):
    # what should be instance_id time?? coord id??
    pass


# get definition of a process/feed/cluster
def entity_definition(type, name):
    #find the 
    pass

# get dependency of a process/feed/cluster
def e_dependency(type, name):
    return {
        "entity": [
            {
                "name": "SampleInput",
                "type": "feed",
                "tag": ['Input']
            },
            {
                "name": "SampleOutput",
                "type": "feed",
                "tag": ['Output']
            },
            {
                "name": "primary-cluster",
                "type": "cluster"
            }
        ]
    }

