import os, sys
import urllib2
import traceback
import httplib
import simplejson as json

class Request():
	
	def send_request(self,request):
		try:
			return urllib2.urlopen(request).read()
		except urllib2.HTTPError, e:
			return json.dumps({'ERROR': 'HTTPError = ' + str(e.code)})
		except urllib2.URLError, e:
			return json.dumps({'ERROR': 'URLError = ' + str(e.reason)})
		except httplib.HTTPException, e:
			return json.dumps({'ERROR': 'HTTPException'})
		except Exception:
			return json.dumps({'ERROR': 'generic exception: ' + traceback.format_exc()})
