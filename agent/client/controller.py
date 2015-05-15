import os
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

