from django.shortcuts import render
import json

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

def parse_feed(xml):
    # you can replace both the following lines with: root = ET.fromstring(country_data_as_string)
    tree = ET.parse('/Users/ajay.yadav/feed.xml')
    root = tree.getroot()
    r = requests.get("http://emerald-oozie.grid.lhr1.inmobi.com:16000/api/entities/definition/feed/"+feed, headers=headers)
    root = ET.fromstring(r.text)


    name = root.attrib['name']
    description = root.attrib.get('description')


    # get all locations for the feed
    locations = []
    for el in root.iter('{uri:falcon:feed:0.1}location'):
        locations.append(el.attrib['path'])
    
    # frequency, 
    frequency = root.find('{uri:falcon:feed:0.1}frequency').text

    # cluster-name, cluster-type,  retention-limit else No Retention , retention-action else No Action
    clusters = []
    for el in root.iter('{uri:falcon:feed:0.1}cluster'):
        cluster = {}
        cluster['name'] = el.attrib['name']
        cluster['type'] = el.attrib.get('type')
        retention = el.find('{uri:falcon:feed:0.1}retention')
        if retention is not None:
            cluster['retention-limit']=retention.attrib['limit']
            cluster['retention-action']=retention.attrib['action']
        else:
            cluster['retention-limit']='No retention'
            cluster['retention-action']='No retention'
        clusters.append(cluster)

    # get all properties
    for property in root.iter('{uri:falcon:feed:0.1}property'):
        if property.attrib['name'].strip() == 'queueName':
            queue = property.attrib['value']
        
        if property.attrib['name'].strip() == 'jobPriority':
            priority = property.attrib['value']

    #finally you should have a dictionary like this
    pass

def parse_cluster(feed):
    pass

def parse_process(feed):
    # parse name
    root = ET.parse('/Users/ajay.yadav/process.xml').getroot()

    name = root.attrib['name']
    description = root.attrib.get('description')
    parallel = root.find('{uri:falcon:process:0.1}parallel').text
    order = root.find('{uri:falcon:process:0.1}order').text
    frequency = root.find('{uri:falcon:process:0.1}frequency').text


    clusters = []
    for el in root.iter('{uri:falcon:process:0.1}cluster'):
        cluster = {}
        cluster['name'] = el.attrib['name']
        validity = el.find('{uri:falcon:process:0.1}validity')
        cluster['start'] = validity.attrib['start']
        cluster['end'] = validity.attrib['end']
        clusters.append(cluster)

    inputs = []
    for el in root.iter('{uri:falcon:process:0.1}input'):
        name = el.attrib.get('name')
        feed = el.attrib['feed']
        start = el.attrib['start']
        end = el.attrib['end']
        partition = el.attrib['partition']
        inputs.append({'name':name, 'feed':feed, 'start':start, 'end':end})

    outputs = []
    for el in root.iter('{uri:falcon:process:0.1}input'):
        name = el.attrib.get('name')
        feed = el.attrib['feed']
        instance = el.attrib['instance']
        outputs.append({'name':name, 'feed':feed, 'instance':instance})

    properties = {}
    for property in root.iter('{uri:falcon:process:0.1}property'):
        properties[property.attrib['name']]=property.attrib['value']


    wf=root.find('{uri:falcon:process:0.1}workflow')
    workflow={'engine':wf.attrib['engine'], 'path':wf.attrib['path'], 'lib':wf.attrib['lib']}

    """
    sample process definition cluster
    {  
        'name':'Sample-Process-Name',
        'description':'Sample process for blah blah blah',
        'frequency':'daily(1)',
        'concurrency':4,
        'order':'LIFO',
        'timeout':'days(1)',
        'retry':{
            'policy':'exponential',
            'attempts':3,
            'after' : 'days(1)'
        },
        'clusters':[{'name':'prod-global', 'start':'2013-12-03T11:00Z', 'end':'2113-12-03T11:00Z'},
                    {'name':'ua-2', 'start':'2013-12-03T11:00Z', 'end':'2113-12-03T11:00Z'}
        ],

        'inputs':[
        {'name':'promotedsupply', 'feed':'CAS-basesummary-promoted, 'start':'today(-71,0)', 'end':'today(-48,50)', 'partition':'*-supply.gz'},
        {'name':'promotedsupply', 'feed':'CAS-basesummary-promoted, 'start':'today(-71,0)', 'end':'today(-48,50)', 'partition':'*-supply.gz'}
        ],

        'outputs':[{'name':'outputraw','feed':'CAS-dwh-daily-raw', 'instance':'today(-72,0)'},
                   {'name':'outputfacts','feed':'CAS-dwh-daily-facts', 'instance':'today(-72,0)'}
        ],

        'properties':{
            'queueName':'reports',
            'jobPriority':'VERY_HIGH',
            'threedaysback':'${formatTime(dateOffset(instanceTime(), -3,'DAY'), 'yyyy-MM-dd')}',
        },
        'workflow':{
            'engine':'oozie',
            'path':'/projects/cas/falcon_flow/dwhdaily/workflow.xml',
            'lib':'/projects/cas/falcon_flow/lib/'
        }
    }
    """

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

def get_process_definition(name):
    process = {  
        'name':'Sample-Process-Name',
        'description':'Sample process for blah blah blah',
        'frequency':'daily(1)',
        'parallel':4,
        'order':'LIFO',
        'timeout':'days(1)',
        'retry':{
            'policy':'exponential',
            'attempts':3,
            'after' : 'days(1)'
        },
        'clusters':[{'name':'prod-global', 'start':'2013-12-03T11:00Z', 'end':'2113-12-03T11:00Z'},
                    {'name':'ua-2', 'start':'2013-12-03T11:00Z', 'end':'2113-12-03T11:00Z'}
        ],

        'inputs':[
          {"name":"promotedsupply", 'feed':"CAS-basesummary-promoted", "start":"today(-71,0)", "end":"today(-48,50)", "partition":"*-supply.gz"},
          {"name":"promotedsupply", 'feed':"CAS-basesummary-promoted", "start":"today(-71,0)", "end":"today(-48,50)", "partition":"*-supply.gz"},
        ],

        'outputs':[{'name':'outputraw','feed':'CAS-dwh-daily-raw', 'instance':'today(-72,0)'},
                   {'name':'outputfacts','feed':'CAS-dwh-daily-facts', 'instance':'today(-72,0)'}
        ],

        'properties':{
            'queueName':'reports',
            'jobPriority':'VERY_HIGH' ,
            'threedaysback':"${formatTime(dateOffset(instanceTime(), -3,'DAY'), 'yyyy-MM-dd')}",
        },
        'workflow':{
            'engine':'oozie',
            'path':'/projects/cas/falcon_flow/dwhdaily/workflow.xml',
            'lib':'/projects/cas/falcon_flow/lib/'
        }
    }
    return process

def get_feeds_list():
    return ['CAS-local-dwh-hourly-facts', 'CAS-rmc-hourly-facts', 'CAS-dwh-daily-facts']

def get_clusters_list():
    return ['HKG-1', 'prod-global','ua-2', 'uj1']

def get_workflows():
    return ['oozie','pig']


def get_feeds_status():
    resp = [
            ["FETL-ImpressionRC-Conversion", "UH1", "1", "NORMAL", "1108", "31", "2", "X", "97.11"],
            ["DP-BaseSummary-promoted-LHR1", "GLOBAL", "30", "NORMAL", "10", "5", "22", "X", "27.03"],
            ["RTBI-Hourly-NetworkFact", "UH1", "60", "NORMAL", "19", "X", "X", "X", "100"],
            ["RTBI-Hourly-SupplyFact", "UH1", "60", "NORMAL", "19", "X", "X", "X", "100"],
            ["DWH-hourly-raw-supply-fact", "GLOBAL", "60", "NORMAL", "9", "3", "6", "X", "50"],
            ["RTBI-minutely-demand", "LHR1", "5", "NORMAL", "110", "36", "82", "X", "48.25"],
            ["RTBI-Hourly-NetworkFact", "LHR1", "60", "HIGH", "19", "X", "X", "X", "100"],
            ["DWH-hourly-raw-network-fact", "GLOBAL", "60", "NORMAL", "2", "8", "8", "X", "11.11"],
            ["user-aged-nid", "GLOBAL", "1440", "NORMAL", "X", "1", "X", "X", "0"],
            ["FETL-beaconenhance", "HKG1", "30", "NORMAL", "26", "6", "6", "X", "68.42"],
            ["FETL-FraudEnhance", "UH1", "30", "NORMAL", "27", "9", "1", "X", "72.97"],
            ["FETL-beaconenhance", "LHR1", "30", "NORMAL", "32", "3", "3", "X", "84.21"],
            ["FETL-beaconenhance", "UJ1", "30", "NORMAL", "28", "4", "6", "X", "73.68"],
            ["user-bssid-location-estimator-sorted", "UH1", "1440", "NORMAL", "X", "X", "X", "X", "NaN"],
            ["user-bssid-location-estimator-sorted", "UJ1", "1440", "NORMAL", "X", "X", "X", "X", "NaN"],
            ["CBP-CLick-Enhance", "HKG1", "1", "NORMAL", "961", "143", "38", "X", "84.15"],
            ["RRNOB-Replication-UJ1", "GLOBAL", "60", "NORMAL", "11", "4", "4", "X", "57.89"],
            ["user-bssid-location-estimator-sorted", "HKG1", "1440", "NORMAL", "X", "X", "X", "X", "NaN"],
            ["user-attributestore-scanner-base64", "GLOBAL", "1440", "NORMAL", "X", "1", "X", "X", "0"],
            ["FETL-FraudEnhance", "LHR1", "30", "HIGH", "14", "8", "15", "X", "37.84"],
            ["RTBI-minutely-supply", "UJ1", "5", "NORMAL", "126", "25", "77", "X", "55.26"],
            ["FETL-ConversionEnhance", "UH1", "30", "NORMAL", "37", "X", "X", "X", "100"],
            ["RTBI-minutely-network", "HKG1", "5", "NORMAL", "201", "5", "22", "X", "88.16"],
            ["DP-BaseSummary-promoted-HKG1", "GLOBAL", "30", "NORMAL", "5", "6", "26", "X", "13.51"],
            ["yoda-hourly-summary-3", "GLOBAL", "60", "NORMAL", "X", "3", "16", "X", "0"]
    ]
    return resp

def get_feed_summary():
    resp = [
            ["2014-07-30 12:00", "2014-07-30 12:00", "2014-07-30 12:00", "2014-07-30 12:00", "SLA failed", "0028764-140224075108681-oozie-oozi-C@1230", "Succeeded" ],
            ["2014-07-30 12:00", "2014-07-30 12:00", "2014-07-30 12:00", "2014-07-30 12:00", "SLA met", "0028764-140224075108681-oozie-oozi-C@1231", "Succeeded" ],
            ["2014-07-30 12:00", "2014-07-30 12:00", "2014-07-30 12:00", "2014-07-30 12:00", "SLA met", "0028764-140224075108681-oozie-oozi-C@1232", "Succeeded" ],
            ["2014-07-30 12:00", "2014-07-30 12:00", "2014-07-30 12:00", "2014-07-30 12:00", "SLA met", "0028764-140224075108681-oozie-oozi-C@1233", "Succeeded" ],
            ["2014-07-30 12:00", "2014-07-30 12:00", "2014-07-30 12:00", "2014-07-30 12:00", "SLA met", "0028764-140224075108681-oozie-oozi-C@1234", "Succeeded" ],
            ["2014-07-30 12:00", "2014-07-30 12:00", "2014-07-30 12:00", "2014-07-30 12:00", "SLA failed", "0028764-140224075108681-oozie-oozi-C@1235", "Succeeded" ],
            ["2014-07-30 12:00", "2014-07-30 12:00", "2014-07-30 12:00", "2014-07-30 12:00", "SLA met", "0028764-140224075108681-oozie-oozi-C@1236", "Succeeded" ],
            ["2014-07-30 12:00", "2014-07-30 12:00", "2014-07-30 12:00", "2014-07-30 12:00", "SLA failed", "0028764-140224075108681-oozie-oozi-C@1237", "Succeeded" ],
            ["2014-07-30 12:00", "2014-07-30 12:00", "2014-07-30 12:00", "2014-07-30 12:00", "SLA met", "0028764-140224075108681-oozie-oozi-C@1238", "Succeeded" ],
            ["2014-07-30 12:00", "2014-07-30 12:00", "2014-07-30 12:00", "2014-07-30 12:00", "SLA failed", "0028764-140224075108681-oozie-oozi-C@1239", "Succeeded" ],
            ["2014-07-30 12:00", "2014-07-30 12:00", "2014-07-30 12:00", "2014-07-30 12:00", "SLA met", "0028764-140224075108681-oozie-oozi-C@1240", "Succeeded" ],
            ["2014-07-30 12:00", "2014-07-30 12:00", "2014-07-30 12:00", "2014-07-30 12:00", "SLA met", "0028764-140224075108681-oozie-oozi-C@1241", "Succeeded" ],
            ["2014-07-30 12:00", "2014-07-30 12:00", "2014-07-30 12:00", "2014-07-30 12:00", "SLA failed", "0028764-140224075108681-oozie-oozi-C@1242", "Succeeded" ],
            ["2014-07-30 12:00", "2014-07-30 12:00", "2014-07-30 12:00", "2014-07-30 12:00", "SLA met", "0028764-140224075108681-oozie-oozi-C@1243", "Succeeded" ],
            ["2014-07-30 12:00", "2014-07-30 12:00", "2014-07-30 12:00", "2014-07-30 12:00", "SLA failed", "0028764-140224075108681-oozie-oozi-C@1244", "Succeeded" ],
            ["2014-07-30 12:00", "2014-07-30 12:00", "2014-07-30 12:00", "2014-07-30 12:00", "SLA met", "0028764-140224075108681-oozie-oozi-C@1245", "Succeeded" ],
            ["2014-07-30 12:00", "2014-07-30 12:00", "2014-07-30 12:00", "2014-07-30 12:00", "SLA failed", "0028764-140224075108681-oozie-oozi-C@1246", "Succeeded" ],
            ["2014-07-30 12:00", "2014-07-30 12:00", "2014-07-30 12:00", "2014-07-30 12:00", "SLA met", "0028764-140224075108681-oozie-oozi-C@1247", "Succeeded" ],
            ["2014-07-30 12:00", "2014-07-30 12:00", "2014-07-30 12:00", "2014-07-30 12:00", "SLA met", "0028764-140224075108681-oozie-oozi-C@1248", "Succeeded" ],
            ["2014-07-30 12:00", "2014-07-30 12:00", "2014-07-30 12:00", "2014-07-30 12:00", "SLA met", "0028764-140224075108681-oozie-oozi-C@1249", "Succeeded" ],
            ["2014-07-30 12:00", "2014-07-30 12:00", "2014-07-30 12:00", "2014-07-30 12:00", "SLA met", "0028764-140224075108681-oozie-oozi-C@1250", "Succeeded" ],
            ["2014-07-30 12:00", "2014-07-30 12:00", "2014-07-30 12:00", "2014-07-30 12:00", "SLA met", "0028764-140224075108681-oozie-oozi-C@1251", "Succeeded" ],
            ["2014-07-30 12:00", "2014-07-30 12:00", "2014-07-30 12:00", "2014-07-30 12:00", "SLA failed", "0028764-140224075108681-oozie-oozi-C@1252", "Succeeded" ],
            ["2014-07-30 12:00", "2014-07-30 12:00", "2014-07-30 12:00", "2014-07-30 12:00", "SLA failed", "0028764-140224075108681-oozie-oozi-C@1253", "Succeeded" ],
            ["2014-07-30 12:00", "2014-07-30 12:00", "2014-07-30 12:00", "2014-07-30 12:00", "SLA met", "0028764-140224075108681-oozie-oozi-C@1254", "Succeeded" ],
            ["2014-07-30 12:00", "2014-07-30 12:00", "2014-07-30 12:00", "2014-07-30 12:00", "SLA met", "0028764-140224075108681-oozie-oozi-C@1255", "Succeeded" ],
            ["2014-07-30 12:00", "2014-07-30 12:00", "2014-07-30 12:00", "2014-07-30 12:00", "SLA met", "0028764-140224075108681-oozie-oozi-C@1256", "Succeeded" ],
            ["2014-07-30 12:00", "2014-07-30 12:00", "2014-07-30 12:00", "2014-07-30 12:00", "SLA met", "0028764-140224075108681-oozie-oozi-C@1257", "Succeeded" ],
            ["2014-07-30 12:00", "2014-07-30 12:00", "2014-07-30 12:00", "2014-07-30 12:00", "SLA met", "0028764-140224075108681-oozie-oozi-C@1258", "Succeeded" ],
            ["2014-07-30 12:00", "2014-07-30 12:00", "2014-07-30 12:00", "2014-07-30 12:00", "SLA met", "0028764-140224075108681-oozie-oozi-C@1259", "Succeeded" ]

    ]
    return resp


def get_process_summary(process_name):
    resp = [
            ["2014-07-30 12:00", "2014-07-30 12:00", "0028764-140224075108681-oozie-oozi-C@1230", "Succeeded" ],
            ["2014-07-30 12:00", "2014-07-30 12:00", "0028764-140224075108681-oozie-oozi-C@1231", "Succeeded" ],
            ["2014-07-30 12:00", "2014-07-30 12:00", "0028764-140224075108681-oozie-oozi-C@1232", "Succeeded" ],
            ["2014-07-30 12:00", "2014-07-30 12:00", "0028764-140224075108681-oozie-oozi-C@1233", "Succeeded" ],
            ["2014-07-30 12:00", "2014-07-30 12:00", "0028764-140224075108681-oozie-oozi-C@1234", "Succeeded" ],
            ["2014-07-30 12:00", "2014-07-30 12:00", "0028764-140224075108681-oozie-oozi-C@1235", "Succeeded" ],
            ["2014-07-30 12:00", "2014-07-30 12:00", "0028764-140224075108681-oozie-oozi-C@1236", "Succeeded" ],
            ["2014-07-30 12:00", "2014-07-30 12:00", "0028764-140224075108681-oozie-oozi-C@1237", "Succeeded" ],
            ["2014-07-30 12:00", "2014-07-30 12:00", "0028764-140224075108681-oozie-oozi-C@1238", "Succeeded" ],
            ["2014-07-30 12:00", "2014-07-30 12:00", "0028764-140224075108681-oozie-oozi-C@1239", "Succeeded" ],
            ["2014-07-30 12:00", "2014-07-30 12:00", "0028764-140224075108681-oozie-oozi-C@1240", "Succeeded" ],
            ["2014-07-30 12:00", "2014-07-30 12:00", "0028764-140224075108681-oozie-oozi-C@1241", "Succeeded" ],
            ["2014-07-30 12:00", "2014-07-30 12:00", "0028764-140224075108681-oozie-oozi-C@1242", "Succeeded" ],
            ["2014-07-30 12:00", "2014-07-30 12:00", "0028764-140224075108681-oozie-oozi-C@1243", "Succeeded" ],
            ["2014-07-30 12:00", "2014-07-30 12:00", "0028764-140224075108681-oozie-oozi-C@1244", "Succeeded" ],
            ["2014-07-30 12:00", "2014-07-30 12:00", "0028764-140224075108681-oozie-oozi-C@1245", "Succeeded" ],
            ["2014-07-30 12:00", "2014-07-30 12:00", "0028764-140224075108681-oozie-oozi-C@1246", "Succeeded" ],
            ["2014-07-30 12:00", "2014-07-30 12:00", "0028764-140224075108681-oozie-oozi-C@1247", "Succeeded" ],
            ["2014-07-30 12:00", "2014-07-30 12:00", "0028764-140224075108681-oozie-oozi-C@1248", "Succeeded" ],
            ["2014-07-30 12:00", "2014-07-30 12:00", "0028764-140224075108681-oozie-oozi-C@1249", "Succeeded" ],
            ["2014-07-30 12:00", "2014-07-30 12:00", "0028764-140224075108681-oozie-oozi-C@1250", "Succeeded" ],
            ["2014-07-30 12:00", "2014-07-30 12:00", "0028764-140224075108681-oozie-oozi-C@1251", "Succeeded" ],
            ["2014-07-30 12:00", "2014-07-30 12:00", "0028764-140224075108681-oozie-oozi-C@1252", "Succeeded" ],
            ["2014-07-30 12:00", "2014-07-30 12:00", "0028764-140224075108681-oozie-oozi-C@1253", "Succeeded" ],
            ["2014-07-30 12:00", "2014-07-30 12:00", "0028764-140224075108681-oozie-oozi-C@1254", "Succeeded" ],
            ["2014-07-30 12:00", "2014-07-30 12:00", "0028764-140224075108681-oozie-oozi-C@1255", "Succeeded" ],
            ["2014-07-30 12:00", "2014-07-30 12:00", "0028764-140224075108681-oozie-oozi-C@1256", "Succeeded" ],
            ["2014-07-30 12:00", "2014-07-30 12:00", "0028764-140224075108681-oozie-oozi-C@1257", "Succeeded" ],
            ["2014-07-30 12:00", "2014-07-30 12:00", "0028764-140224075108681-oozie-oozi-C@1258", "Succeeded" ],
            ["2014-07-30 12:00", "2014-07-30 12:00", "0028764-140224075108681-oozie-oozi-C@1259", "Succeeded" ]

    ]
    return resp
