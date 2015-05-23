import os, dirs, random
import urllib, urllib2
import simplejson as json
from procs import Procs
from request import Request
from container.container import Container
from collections import defaultdict

_NET_IF_ = 'docker0'
_CONTAINERS_ = '/root/containers.list'
_HOSTS_FILE_ = '/etc/hosts'
_HOSTS_ = '/root/hosts'

class VirtualEthernet():

	# init
	def __init__(self):
		# initialization
		self.proc = Procs()
		self.request = Request()
		self.local_ip = self.proc._exec("ifconfig eth0 | grep 'inet addr:'").split(":")[1].split(" ")[0]
		self.container_obj = Container()
        
	# get docker bridge ip address
	def get_docker_br(self):
		return self.proc._exec("ifconfig %s | grep 'inet addr:'"%(_NET_IF_ )).split(":")[1].split(" ")[0]
		
	# get container ip
	def get_container_ip(self, container_id):
		return self.proc._exec("sudo docker inspect %s | grep IPAddress"%(container_id)).split(":")[1].split(',')[0].replace('"','').replace(" ",'')

	# assgin ip address
	def assgin_ip_addr(self,interface, ip):
		return self.proc._exec("ip a add %s dev %s"%(ip, interface)) 

	# get all veth interfaces
	def get_network_interfaces(self):
		ifc = []
		try:
			interfaces = self.proc._exec("ifconfig | grep veth").split('\n')
			for interface in interfaces:
				tmp_ifc = interface.split(' ')[0].replace(' ','')
				if tmp_ifc != '':
					ifc.append(tmp_ifc)
		except:
			pass
		return ifc
	# get interface ip
	def get_interface_ip(self, interface):
		return self.proc._exec("echo `ifconfig %s 2>/dev/null|awk '/inet addr:/ {print $2}'|sed 's/addr://'`"%(interface)).split("\n")[0]			
	# get containers
	def get_containers(self, hosts, response={}):
		containers = []
		for host in hosts:
			# get all container running on this host
			try:
				if host !=self.local_ip:
					containers = json.loads(self.request.send_request("http://%s/get_pot"%(host)))
					docker_res = json.loads(self.request.send_request("http://%s/docker_ip"%(host)))
					try:
						if 'docker_ip' in docker_res:
							docker_ip = docker_res["docker_ip"]
					except:
						docker_ip = "Unknown Docker ip"
					
				else:
					containers = self.container_obj.get_containers()
					docker_ip = self.get_docker_br()
				response[host] = {}
				response[host]['containers'] = []
				for container in containers:
					if host == self.local_ip:
						container_ip = self.get_container_ip(container["Id"][:12])
						for interface in self.get_network_interfaces():
							if self.get_interface_ip(interface) == container_ip:
								veth = interface
					else:
						try:
							res = json.loads(self.request.send_request("http://%s/container?id=%s&ip=True"%(host,container["Id"])))
							veth_res = json.loads(self.request.send_request("http://%s/container?id=%s&veth=True"%(host, container["Id"])))
							if "ip_address" in res:
								container_ip = res["ip_address"]
							if "veth" in veth_res:
								veth = veth_res["veth"]
						except:	
							container_ip = "Unkown IP address"
					try:
						container_dict = {'hostname': container["Id"][:12],'interface': veth,'ip_address': container_ip}
						response[host]['containers'].append({container["Id"] :container_dict})
					except:
						pass

				response[host]['bridge_name'] = 'docker0'
				response[host]['bridge_ip'] = docker_ip
			except:	
				pass
			
		return response
	# get hosts list
	def get_hosts(self, hosts=[]):
		if os.path.exists(_HOSTS_):
			file = open(_HOSTS_)
			for line in file.readlines():
				hosts.append(line.split('\n')[0])
		return hosts				


#veth_client = VirtualEthernet()
#print veth_client.get_hosts()
#print veth_client.get_network_interfaces()
#if veth_client.get_interface_ip("teh0") == '':
#	print "None"
#print veth_client.get_containers(['192.168.1.7','192.168.1.8','192.168.1.9'])
