import os
import sys
import containerService as cs
_IMAGE_ = 'ubuntu'

clientObj = cs.containerEngine()
client = clientObj.newClient()

## Create new container
#----------------------
#id = clientObj.createContainer(client,_IMAGE_)
#clientObj.startContainer(client,id)
#print client.containers()

## search image
#--------------
#print clientObj.searchImage(client,'django')
## pullimage
#-----------
clientObj.pullImage(client, 'dockerfiles/django-uwsgi-nginx')

