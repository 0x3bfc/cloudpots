#!/usr/bin/env python
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
import os, sys, requests, json
from flask import request
from flask import Flask, session, render_template
import subprocess

pot = Flask(__name__,  static_url_path = "/imgs", static_folder = "%s/imgs"%(os.path.dirname(os.path.abspath(__file__))))



# generate random key for flask session
pot.secret_key = os.urandom(24)



# execute command line
def run(command):
	pipe = subprocess.PIPE
	p = subprocess.Popen(command,stdout=pipe,stderr=pipe,shell=True)
	return p.stdout.read()+"\n"+p.stderr.read()

# main page
@pot.route('/')
def index():
	return render_template('index.html')


@pot.route('/exec')
def execute():
	command = "bash /pots/bootstrap.sh"
	try:
		if 'cmd' in request.args:
			command = request.args['cmd']
		return json.dumps({'command': run(command)})
	except:
		return json.dumps({'ERROR':'expected command line'})


if __name__ == '__main__':
	pot.run()
