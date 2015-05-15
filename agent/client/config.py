import os
from ConfigParser import ConfigParser
from configobj import ConfigObj

_config_file = 'resource.conf'

class Configuration():

	def __init__(self):
		self._config = ConfigParser()

	def load_config(self, filename):
		if os.path.exists(filename):
			self._config.read(filename)
			return self._config._sections
		else:
			return None
	
	def reset_config(self, filename, configurations):
		config = ConfigObj()
		for k,v in configurations.iteritems():
			print k,v
		if os.path.exists(filename):
			config.filename = filename
			config['RESOURCES'] = {}
			config['RESOURCES']['cpu'] = configurations['RESOURCES']['cpu']
			config['RESOURCES']['mem'] = configurations['RESOURCES']['mem']
			config['RESOURCES']['ports'] = configurations['RESOURCES']['ports']
			config.write()
			return True
		else:
			return False
			

