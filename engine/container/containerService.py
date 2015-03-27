import simplejson as json
from docker import Client

_DOCKER_BASEURL_= 'unix://var/run/docker.sock'

class containerEngine():

	def __init__(self):
		self.ports = [22]

	def newClient(self,base_url=_DOCKER_BASEURL_):
		return Client(base_url)
	
	def createContainer(self,client, image_id,ports=None,command=None,mem_limit=None,cpu_shares=None):
		return client.create_container(image_id, command, ports=ports,mem_limit=mem_limit,cpu_shares=cpu_shares)

	def startContainer(self,client, container_id, port_bindings={}):
		return client.start(container_id,port_bindings)
	
	def searchImage(self, client, image_id):
		try:
			return client.search(image_id)[0]
		except:
			return []
	def pullImage(self, client, image_id):
		try:
			for line in client.pull(image_id, stream=True):
				print(json.dumps(json.loads(line), indent=4))
		except:
			raise Exception('Unable to make repository pull request !!')
