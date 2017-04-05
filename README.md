# fib-web-loader

### Requires pykube
`$ pip install pykube`

### Create cluster 
`$ ./create_autoscaling_cluster.sh`

### Add web application that computes fibonacci numbers naively 
`$ kubectl apply -f kubernetes/fibloader.yml`

### When ready to add load deploy the load generator
`$ kubectl apply -f load-gen/kubernetes/fibloadgen.yml`

### To use the api via python you'll need to run the local proxy. 
`$ kubectl proxy `

### After a while determine load distribution
`$ python determine_load_distribution.py`