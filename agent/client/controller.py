import os, urllib2
from procs import Procs
from config import Configuration

_RESOURCES_ = '%s/resources.conf'%(os.path.dirname(os.path.abspath(__file__)))

class Controller():

	def __init__(self):
		self.machine_client = Procs()
		self.configurations = Configuration()

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
		if self.check_connectivity(remote_host_ip):
			if 'error' not in self.machine_client._exec('bash %s/networking/ovs-script.sh %s %s'%(os.path.dirname(os.path.abspath(__file__)), docker_ip, remote_host_ip)):
				return True
			return False
		return False

