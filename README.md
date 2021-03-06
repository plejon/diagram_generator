# diagram generator
This is based on the python lib diagrams.  
see ```requirements.txt```

#### how to run
```bash
$ python3 main.py example.yml
$ ./main.py example.yml
```
#### example
```yaml
---
diagram_name: "mydiagram" # required, name of the diagram
Azure: # cluster
  dev: # child cluster with nodes
    sql:
      - diagrams.azure.compute.VMWindows # first list entry always specify node icon shape
      # all following  indices specify connection points to other nodes/clusters
      - elastic
    win:
      - diagrams.azure.compute.VMWindows
      - sql
      - mail
      - {"rabbitmq": "TCP/5672\nTCP/5555"} # dict specify connection with label. looks awful in big diagrams
      - elastic
    elastic:
      - diagrams.azure.compute.VMLinux
      - sql
    mail:
      - diagrams.azure.compute.VMLinux
    rabbitmq:
      - diagrams.azure.compute.VMLinux
      - ["host1"]
    k8s clusters: # grand child cluster
      k8s:
        - diagrams.azure.compute.KubernetesServices
        - win
        - rabbitmq
annother cluster:
  host1:
    - diagrams.azure.compute.VMWindows
```
Output from above yaml
![result](./mydiagram.png)