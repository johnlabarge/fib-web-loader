import operator
import pykube
import os

#class HostsAndRegions:   
api = pykube.HTTPClient(pykube.KubeConfig.from_url('http://localhost:8001'))



nodes=pykube.Node.objects(api)


# Dictionary that will map each Node to a Zone,
# It will be used when dealing with pods and logs.
nodezone = {} 

# Count how many nodes there are in each zone,
# Iterating over all the nodes.
# Note that not all nodes may have pods for the fibloader service.
nodes_in_zone = {}
for node in nodes: 
  zone = node.metadata['labels']['failure-domain.beta.kubernetes.io/zone']
  nodezone[node.name] = zone
  if zone in nodes_in_zone: 
    count = nodes_in_zone[zone] + 1
  else: 
    count = 0 + 1
  nodes_in_zone[zone] = count 



# Count how many requests were logged by the fibloader service per zone,
# by iterating over all the fibloader pods and their logs, mapping node to zone.
# It will also count how many pods there are per zone, based on pod's node
requests_by_zone = {}
pods_in_zone = {}
 
for node in nodes: 
  zone = nodezone[node.name]
  if zone not in requests_by_zone: 
    requests_by_zone[zone] = 0
  if zone not in pods_in_zone:
    pods_in_zone[zone] = 0

pods = pykube.Pod.objects(api)
pods = filter(operator.attrgetter("ready"),pods)

for pod in pods: 
  if "fibloader" in pod.name: # and pod.Status == 'Running':
    host = None
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
    if  host == None:
      host = pod.obj["spec"]["nodeName"]
    zone = nodezone[host]
    if pods_in_zone:
      count = pods_in_zone[zone]
      count = count + 1
      pods_in_zone[zone] = count

print "zone\t\t| nodes in zone\t| pods in zone\t| requests"
for zone in requests_by_zone.keys(): 
    print "{0}\t| {1}\t\t| {2}\t\t| {3}".format(zone, nodes_in_zone[zone], pods_in_zone[zone], requests_by_zone[zone])
