#    Copyright 2015 CloudPOTS.

#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

#    POTS Manager API services will return a JSON-encoded response for your running 
#    containers. Check out CloudPOTS https://github.com/aabdulwahed/cloudpots . 
#    To fiddle with a JSON response, requests includes a json() method for the 
#    response object, which can be acessed like a regular dict

import os, sys, requests, dirs, json
from flask import request
from flask import Flask, session, render_template
from container.container import Container
from controller import Controller

 
manage = Flask(__name__,  static_url_path = "/imgs", static_folder = "%s/imgs"%(os.path.dirname(os.path.abspath(__file__))))

# generate random key for flask session
manage.secret_key = os.urandom(24)

# defualt settings also used for testing 
_DEFUALT_IMAGE_ = 'ahmedabd/cloudpot:v8'
_CPU_		= 1
_MEM_		= 1
_PORTS_ 	= {5000: 5000, 22:2200, 80:8000 }
_COMMAND_	= None

# create container
@manage.route('/create')
def create_pot():

	global _CPU_, _MEM_,_DEFUALT_IMAGE_, _PORTS_, _COMMAND_	

	# required resources per container 
	# 1 CPU, 1 GRAM , defualt image, ports
	try:
		if 'cpu' in request.args:
			_CPU_ = request.args['cpu']
		if 'mem' in request.args:
			_MEM_ = request.args['mem']
		if 'image' in request.args:
			_DEFUALT_IMAGE_ = request.args['image']
	except:
		pass

	# configure container resources
	acq_resources = {'cpu':_CPU_,'mem':_MEM_}
	c = Container()
	controller = Controller()
	resources = controller.check_resource_availability()

	# configure container ports
	# _PORTS_         = {5000: 5000, 22:2200, 80:8000 }
	private_ports = []
	container_endpoints = {}
	port_order = controller.resources['RESOURCES']['ports']
	for key, val in _PORTS_.iteritems():
		private_ports.append(key)
		container_endpoints[key] = int(str(val)[:-1] + port_order)

	#try:
	if resources != None:
			if int(resources['cpu']) > 0 and float(resources['mem']) > 0:

				# initiate and start container 
				r = c.create_container(_DEFUALT_IMAGE_, 
							command= _COMMAND_, 
							cpu=str(acq_resources['cpu']), 
							mem='%sg'%(str(acq_resources['mem'])), 
							private_ports= private_ports, 
							container_endpoints = container_endpoints)

				# set new resources in resources.conf
				cpu_resources = int(controller.resources['RESOURCES']['cpu']) + int(acq_resources['cpu'])
				mem_resources = float(controller.resources['RESOURCES']['mem']) + float(acq_resources['mem'])
				print str(int(controller.resources['RESOURCES']['ports']) + 1)
				controller.set_resources({'RESOURCES':{'cpu': cpu_resources, 
					 			'mem': mem_resources,
								'ports': int(controller.resources['RESOURCES']['ports']) + 1}})

				return json.dumps(r, indent=4)

		# avoid any resource capacity violation		
	return json.dumps({'ERROR':'Unavailable resources, scale out your infrastructure, available capacity is CPU: %s, MEM: %s'%(resources['cpu'],resources['mem'])})

	#except IOError as (errno, strerror):
	#	return json.dumps({'ERROR': 'I/O error({0}): {1}'.format(errno, strerror)})
	#except:
	#	return json.dumps({'ERROR':'Unexpected Error "%s" '%(sys.exc_info()[0])})


# remove containers
@manage.route('/remove_containers')
def remove_containers():
	container_client = Container()
	containers = get_all_containers()
	deleted_containers = []
	if len(containers) >0:
		for container in containers:
			if container_client.remove_container(container):
				deleted_containers.append(container["Id"])
	# reset resource configurations
	controller = Controller()
	controller.set_resources({'RESOURCES':{'cpu': 1,
				'mem': 0, 'ports':0}})	
	return json.dumps({'INFO': '200 OK','deleted':deleted_containers}, indent=4)	



# get list of running containers
def get_all_containers():
	container_obj = Container()
        container_details = container_obj.get_containers()
	return container_details

# get containers
@manage.route('/get_pot')
def get_pot():
        container_resources = get_all_containers()
	if len(container_resources) !=0:
        	return json.dumps(container_resources, indent=4)
	return json.dumps({'INFO': 'There is no available container, setup new container'}, indent=4)


# list all images
@manage.route('/images')
def images():
	container_obj = Container()
	return json.dumps( container_obj.list_images(image=None), indent=4)


# pull image to local repo
@manage.route('/pull')
def pull_image():
	client = Container()
	try:
		if 'image' in request.args:
			image = request.args['image']
		return json.dumps(client.pull_image(image))
	except:
		return json.dumps({"ERROR":"Expected image name"})


# main page
@manage.route('/')
def index():
	return render_template('index.html')

if __name__ == '__main__':
	#print create_pot()
	#raise Exception()
	manage.run( 
		host="0.0.0.0",
		port=int("80")
	)
