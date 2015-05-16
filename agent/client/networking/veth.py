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
		self.proc = Procs()
 
	# get docker bridge ip address
	def get_docker_br(self):
		return self.proc._exec("ifconfig %s | grep 'inet addr:'"%(_NET_IF_ )).split(":")[1].split(" ")[0]


	# check availability of container ip
	def check_availability(self, container_ip, ip_list=[]):
		for line in self.proc._exec("ifconfig | grep 'inet addr:'").split('\n'):
			try:
				ip_list.append(line.split(":")[1].split(" ")[0])
			except:
				pass
		for ip in ip_list:
			if ip.replace(' ','') == container_ip:
				return True
		return False

	# get random container ip
	def get_random_ip(self, docker_ip):
		try:
			k = 0
			while(1):
				docker_prefix = '.'.join(docker_ip.split('.')[:-1])
				container_ip = '.'.join([docker_prefix,str(random.randint(1,254))])
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
	def get_containers(self, containers_json = {}):
		if os.path.exists(_CONTAINERS_):
			with open(_CONTAINERS_) as datafile:
				containers_json = json.loads(datafile.read())
		return containers_json
	
	# get virtual eth
	def get_veths(self, veths=[]):
		lines = self.proc._exec("ifconfig | grep 'veth'").split('\n')
		for line in lines:
			if line.split(' ')[0] != '':
				veths.append(line.split(' ')[0])
		return veths

	# modify containers list
	def modify_containers_list(self, container_id, container_ip, node_ip, veth, docker_ip):
		
		containers_json = self.get_containers()
		
		bridge = "br0"
		containers_json[container_id] = {
					'container_ip':container_ip,
					'veth': veth,
					'node_ip': node_ip,
					'docker_ip': docker_ip,
					'bridge': bridge}
		# modify /etc/hosts
		self.configure_hosts_file(containers_json)

		with open( _CONTAINERS_, 'w') as outputfile:
			outputfile.write(json.dumps(containers_json))

	# broadcast containers list to all cluster's nodes
	def broadcast_containers_list(self, local_ip ,json_file = _CONTAINERS_):

		if self.broadcast(local_ip, self.get_containers()) != None:
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
		for key, value in containers.iteritems():
			#raise Exception(containers[key]['node_ip'])
			hosts_list += "%s\t%s\n"%(containers[key]['node_ip'], 'host1')
			hosts_list += "%s\t%s\n"%(containers[key]['container_ip'],'container1')

		hosts_file = open(_HOSTS_FILE_, 'w')
		hosts_file.write(hosts_list)

veth_obj = VirtualEthernet()

if veth_obj.check_availability('172.18.0.1'):
	print "exist"
else: 
	print "not"


veths = veth_obj.get_veths()
ip =  veth_obj.get_random_ip(veth_obj.get_docker_br())
#print veth_obj.get_containers()
veth_obj.modify_containers_list("9f6f34a4934b6a5430960c81171bd5b1b9580fd454d266e28e1c2e4833f31341", ip, '192.168.1.7', veths[0], veth_obj.get_docker_br())
#print veth_obj.connect_container(ip, 'docker0')
