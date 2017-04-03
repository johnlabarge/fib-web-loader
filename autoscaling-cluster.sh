#!/bin/sh

#ASSUMES DEFAULT CREDENTIALS AVAILABLE
gcloud container clusters create cluster-under-test --zone us-central1-f --additional-zones=us-central1-a,us-central1-b --enable-autoscaling --min-nodes=1 --max-nodes=36 --log-http


# outputs: TODO use deployment manager to create 
# {"cluster": 
#    {
#       "locations": ["us-central1-a", "us-central1-b", "us-central1-f"], 
#       "masterAuth": {"username": "admin"}, 
#       "name": "cluster-under-test", 
#       "nodePools": [
#           {
#               "autoscaling": {"enabled": true, "maxNodeCount": 12, "minNodeCount": 1}, 
#               "config": {
#                   "oauthScopes": ["https://www.googleapis.com/auth/compute", "https://www.googleapis.com/auth/devstorage.read_only", "https://www.googleapis.com/auth/service.management.readonly", "https://www.googleapis.com/auth/servicecontrol"]
#                }, 
#               "initialNodeCount": 3,
#               "name": "default-pool"}
#       ]
#     }
# }
