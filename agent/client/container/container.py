import os,sys
from services import ContainerEngine

_IMAGE_ = 'ubuntu'
_IMAGE_ = 'dockerfiles/django-uwsgi-nginx'

class Container():

	def __init__(self):
		self.clientObj = ContainerEngine()
		self.client = self.clientObj.newClient()

	def create_container(self, 
			  	image=_IMAGE_, 
			  	command= None, 
				cpu = None, 
				mem = None,
				private_ports= [],
				container_endpoints = {}):

	
		# check image availablility on local repo
		found = False
		for i in self.list_images():
			if image in i["RepoTags"][0]:
				found = True
		# download image
		if not found:
			self.pull_image(image=image)
		
		# initiate container
		id = self.clientObj.createContainer(self.client,
							image, 
							command = command,  
							mem_limit = mem, 
							cpu_shares = cpu,
							private_ports = private_ports)
		# start container
		self.clientObj.startContainer(self.client,id['Id'], container_endpoints = container_endpoints)

		containers =  self.client.containers()
		for container in containers:
			if container['Id'] == id['Id']:
				return container
		return {}

	def get_containers(self):
		# get list of running containers
		return self.client.containers()

	def remove_container(self, container):
		return self.clientObj.removeContainer(self.client, container['Id'])

	def list_images(self, image=None):
		return self.clientObj.list_images(self.client, image=image)

	def pull_image(self, image='dockerfiles/django-uwsgi-nginx'):
		return self.clientObj.pullImage(self.client, image)

