import simplejson as json
from docker import Client

_DOCKER_BASEURL_= 'unix://var/run/docker.sock'
_PORTS_ = [2200]

class ContainerEngine():

	def __init__(self):
		self.ports = [22]

	def newClient(self,base_url=_DOCKER_BASEURL_):
		return Client(base_url)
	
	def createContainer(self,client, 
				image_id,
				command=None, 
				mem_limit=None, 
				cpu_shares=None,
				private_ports = []):

		"""Initiate and Create Container"""
		return client.create_container(image_id,
						command, 
						detach=True,
						ports = private_ports ,
						mem_limit=mem_limit,
						cpu_shares=cpu_shares)

	def startContainer(self,client, container_id, container_endpoints={}):

		"""Start Container"""
		return client.start(container_id, port_bindings = container_endpoints)
	
	def searchImage(self, client, image_id):

		"""Search Public Image Repo -- docker hub"""
		try:
			return client.search(image_id)[0]
		except:
			return {'ERROR':'Image is not found'}

	def pullImage(self, client, image_id):

		"""Pull Image from Public Repo"""
		try:
			for line in client.pull(image_id, stream=True):
				print(json.dumps(json.loads(line), indent=4))
			return self.list_image(client,image=image_id)
		except:
			return {'ERROR':'Unable to pull image with a record id "%s" from docker hub!!'%(image_id)}

	def list_images(self, client, image=None):

		"""list local repo images"""
		if image != None:
			return client.images(image=image)
		return client.images()

	def removeContainer(self, client, container):

		"""stop container then remove the stopped one"""
		client.stop(container)
		client.remove_container(container)
		return True

