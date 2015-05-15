#!/usr/bin/python
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

from setuptools import setup

setup(
	name='cpot-manager',
	version='0.1',
	description='CLOUDPOTS provides creating container based clusters',
	author='Ahmed Abdullah', author_email='info@cloudpots.com',
	url='http://cloudpots.com/',
	install_requires=['flask', 'requests','docker-py','configobj']
)
