import os, dirs, random
import urllib, urllib2
import simplejson as json
from procs import Procs


_NET_IF_ = 'docker0'
_CONTAINERS_ = '/root/containers.list'
_HOSTS_FILE_ = '/etc/hosts'


class VirtualEthernet():

	# init
	def __init__(self):
		# initialization
		self.proc = Proc()
 
	# get docker bridge ip address
	def get_docker_br(self):
		return self.proc._exec("ifconfig %s | grep 'inet addr:'"%(_NET_IF_ )).split(":")[1].split(" ")[0]


	# check availability of container ip
	def check_availability(self, container_ip):
		for line in self.proc._exec("ifconfig | grep 'inet addr:'").split('\n')
			ip_list.append(line.split(":")[1].split(" ")[0])
		for ip in ip_list:
			if ip.replace(' ','') == container_ip:
				return True
		return False

	# get random container ip
	def get_random_ip(self, docker_ip):
		try:
			k = 0
			while(1):
				container_ip = '.'.join(docker_ip.split('.')[:-1],random.randint(1,254))
				if not self.check_availability(container_ip):
					return container_ip
				if k >= 254:
					break
				k +=1
		except:
			return None

	# connect container to docker bridge
	def connect_container( self, ip_addr, docker_br):
		if 'error' in  self.proc._exec("ip addr add %s dev %s"%(ip_addr, docker_br)):
			return False
		return True

	# get containers
	def get_containers(self, containers_json = None):
		if os.path.exists(_CONTAINERS_):
			with open(_CONTAINERS_) as datafile:
				containers_json = json.loads(datafile)
		return containers_json
	
	# get virtual eth
	def get_veths(self, veths=[]):
		lines = self.proc._exec("ifconfig | grep 'veth'").split('\n')
		for line in lines:
			veths.append(line.split(' ')[0])
		return veths

	# modify containers list
	def modify_containers_list(self, container_id, container_ip, node_ip, veth, docker_ip):
		
		containers_json = self.get_containers()

		containers_json[container_id] = {
					'container_ip':container_ip,
					'veth': veth,
					'node_ip': node_ip,
					'docker_ip': docker_ip,
					'bridge': 'br0'
					}
		# modify /etc/hosts
		self.configure_hosts_file(containers_json)

		with open( _CONTAINERS_, 'w') as outputfile:
			json.dumps(containers_json)

	# broadcast containers list to all cluster's nodes
	def broadcast_containers_list(self, local_ip ,json_file = _CONTAINERS_):

		if os.path.exists(json_file):
			with open(json_file) as datafile:
				containers_json = json.loads(datafile)
			if self.broadcast(local_ip, containers_json) != None:
				return True
		return False

	# broadcast messages using POST method			
	def broadcast(self, local_ip, data):
		broadcast_status = None
		for key, val in data.iteritems():
			if local_ip != data[key]['node_ip']:
				post_data = urllib.urlencode(data)
				req = urllib2.Request('http://%s/broadcast'%(data[key]['node_ip']), post_data)
				response = urllib2.urlopen(req)
				if response.read() == 'OK':
					broadcast_status[data[key]['node_ip']] = True
				else:
					broadcast_status[data[key]['node_ip']] = False
		return broadcast_status
					
	# configure /etc/hosts
	def configure_hosts_file(self, containers):
		hosts_list = ""
		for key, value in containers:
			hosts_list += "%s\t%s\n"%(containers[key]['node_ip'])
			hosts_list += "%s\t%s\n"%(containers[key]['container_ip'])

		hosts_file = open(_HOSTS_FILE_, 'w')
		hosts_list.write(hosts_list)							
