# Network Configurations
------------------------

Ovs-script.sh is used to djust the REMOTE_IP and BRIDGE_ADDRESS variables. The BRIDGE_NAME can be the same on hosts. 
This is illustrated by the following steps:



1. Every container run with Docker is attached to docker0 bridge. This is a regular bridge you can create on every Linux system, without the need for Open vSwitch.

2. The docker0 bridge is attached to another bridge: br0. This time it’s an Open vSwitch bridge. This means that all traffic between containers is routed through br0 too. You can think about two switches connected to each other.

3. Additionally we need to connect together the networks from both hosts in which the containers are running. A GRE tunnel is used for this purpose. This tunnel is attached to the br0 Open vSwitch bridge and as a result to docker0 too.


#Ring Netowrk using post request to connect multiple nodes: 

	curl -i -H "Content-Type: application/json" -X POST -d '{"hosts":["192.168.1.7","192.168.1.8", "192.168.1.9"]}' http://192.168.1.7/ring


Result

	{"192.168.1.7": {"status": {"connected": true}, "docker_addr": "172.17.0.1"}, "192.168.1.9": {"status": {"connected": true}, "docker_addr": "172.17.2.1"}, "192.168.1.8": {"status": {"connected": true}, "docker_addr": "172.17.1.1"}}
