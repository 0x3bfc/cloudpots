import os, urllib2, time
from procs import Procs
from config import Configuration
import simplejson as json 
#import logging as checksLogger

#checksLogger.basicConfig(filename='/root/pots.log',level=logging.DEBUG)



_RESOURCES_ = '%s/resources.conf'%(os.path.dirname(os.path.abspath(__file__)))
_DOCKER_ADDR_ = '172.17.0.1'
_NET_IF_ = "eth0"
 
class Controller():

	def __init__(self):
		self.machine_client = Procs()
		self.configurations = Configuration()
		self.local_ip = self.machine_client._exec("ifconfig %s | grep 'inet addr:'"%(_NET_IF_ )).split(":")[1].split(" ")[0]
		try:
			self.available_resources = {'cpu': self.machine_client._cpu_count(),
						    'mem': self.machine_client._mem_size()}
			self.resources = self.configurations.load_config(_RESOURCES_)
		except (ImportError, AttributeError):
			pass 

	# check total available resources
	def check_resource_availability(self):
		try:
			resources = self.configurations.load_config(_RESOURCES_)
			resources_dict =  {'cpu': int(self.available_resources['cpu']) - int(resources['RESOURCES']['cpu']),
				'mem': float(self.available_resources['mem']) - float(resources['RESOURCES']['mem'])}
			return resources_dict
		except(AttributeError):
			return None

	# set resources in resources.conf
	def set_resources(self, resources):
		if self.configurations.reset_config(_RESOURCES_, resources):
			return True
		return False
	
	# check connectivity
	def check_connectivity(self, remote_host_ip):
		try:
			response = urllib2.urlopen('http://%s'%(remote_host_ip),timeout=1)
			return True
		except:
			return False	
		

	# connecting hosts 
	def connect_host(self, docker_ip, remote_host_ip):
		if 'error' not in self.machine_client._exec('bash %s/networking/ovs-script.sh %s %s'%(os.path.dirname(os.path.abspath(__file__)), remote_host_ip, docker_ip)):
			return True
		return False

	# connect pots ring
	def connect_ring(self, hosts):
		ring_addresses = {}
		i = 0
		# prepare hosts dictionary and check remote hosts connectivity
		for  addr in hosts:
			docker_addr = _DOCKER_ADDR_.split('.')
			docker_addr[2] = str(i)
			k = 0
			while(1):
				if self.local_ip == addr:
					ring_addresses[addr] = '.'.join(docker_addr)
					break
				elif self.check_connectivity(addr):
					ring_addresses[addr] = '.'.join(docker_addr)
					break
				else:
					time.sleep(2)
				if k > 5:
					break
				k +=1
			i +=1
		# assign remote host and connect the ring
		addr_index = 0
		ring = {}		
		for host in hosts:
			if host == self.local_ip:
				response = self.connect_host(ring_addresses[host], hosts[addr_index+1])
				response = json.dumps({'connected':response})
			elif addr_index < len(hosts) -1:
				response = self.get_ring_response(host, ring_addresses[host], hosts[addr_index+1])
				#self.connect_host(ring_addresses[host], hosts[add_index+1])
			else:
				response = self.get_ring_response(host, ring_addresses[host], hosts[0])
				#self.connect_host(ring_addresses[host], hosts[0])
			ring[host] = {'docker_addr': ring_addresses[host], 'status':json.loads(response)}
			addr_index +=1

		return ring	
		

	# get ring response
	def get_ring_response(self, host, docker_addr, remote_host):
		try:
			json_response = urllib2.urlopen("http://%s/connect?docker_addr=%s&remote_host=%s"%(host, docker_addr, remote_host)).read()
			return json_response
		except urllib2.HTTPError, e:
			#checksLogger.error('HTTPError = ' + str(e.code))
			return json.dumps({'ERROR': 'HTTPError = ' + str(e.code)})
		except urllib2.URLError, e:
			#checksLogger.error('URLError = ' + str(e.reason))
			return json.dumps({'ERROR': 'URLError = ' + str(e.reason)})
		except httplib.HTTPException, e:
			#checksLogger.error('HTTPException')
			return json.dumps({'ERROR': 'HTTPException'})
		except Exception:
			import traceback
			#checksLogger.error('generic exception: ' + traceback.format_exc())
			return json.dumps({'ERROR': 'generic exception: ' + traceback.format_exc()})
