#!/bin/bash
# THIS BASH SCRIPT IS USED TO CONFIGURE NETOWORKING
# BETWEEM MULTIPLE PHYSICAL HOSTS TO PROVIDE THE 
# CONNECTIVITY AMONG DOCKER CONTAINERS OVER TRADITIONAL
# SERVICE PROVIDER NETWORKS USING DOCKER BRIDGE AND OPENVSWITCH


# Remote Host IP
REMOTE_IP=$1
# Docker Bridge Name
BRIDGE_NAME=docker0
# Docker Bridge IP
BRIDGE_ADDRESS=$2/24


# Make Docker Bridge Down
ip link set $BRIDGE_NAME down
# Delete Docker Bridge
brctl delbr $BRIDGE_NAME
# Delete Default OpenvSwitch Bridge br0
ovs-vsctl del-br br0
# Add Docker Bridge
brctl addbr $BRIDGE_NAME
# Assgin new Ip address to Docker bridge
ip a add $BRIDGE_ADDRESS dev $BRIDGE_NAME
# Make Docker Bridge Link up
ip link set $BRIDGE_NAME up
# Add Default OpenvSwitch Bridge br0
ovs-vsctl add-br br0
# Create the tunnel to the other host and attach it to the
# br0 bridge
ovs-vsctl add-port br0 gre0 -- set interface gre0 type=gre options:remote_ip=$REMOTE_IP
# Add the br0 bridge to docker0 bridge
brctl addif $BRIDGE_NAME br0


# stop Docker Service
service docker stop
# start Docker Service
service docker start
