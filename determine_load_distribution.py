import operator
import pykube
import os

#class HostsAndRegions:   
api = pykube.HTTPClient(pykube.KubeConfig.from_url('http://localhost:8001'))







nodes=pykube.Node.objects(api)
nodezone = {} 
 
nodes_in_zone = {}
for node in nodes: 
  zone = node.metadata['labels']['failure-domain.beta.kubernetes.io/zone']
  nodezone[node.name] = zone
  if zone in nodes_in_zone: 
    count = nodes_in_zone[zone] + 1
  else: 
    count = 0
  nodes_in_zone[zone] = count 

requests_by_zone = {}
 
for node in nodes: 
  zone = nodezone[node.name]
  if zone not in requests_by_zone: 
    requests_by_zone[zone] = 0
pods = pykube.Pod.objects(api)
pods = filter(operator.attrgetter("ready"),pods)
for pod in pods: 
  if "fibloader" in pod.name: # and pod.Status == 'Running':
    logs = pod.logs()
    log_lines = logs.split() 
    for log_line in log_lines: 
      if log_line and ":" in log_line:
        host = log_line.split(":")[1] 
        zone = nodezone[host]
        if requests_by_zone: 
          count = requests_by_zone[zone]
          count = count + 1
          requests_by_zone[zone] = count 

print "zone\t\t| nodes in zone\t| requests"
for zone in requests_by_zone.keys(): 
    print "{0}\t| {1}\t\t| {2}".format(zone,nodes_in_zone[zone],requests_by_zone[zone])
