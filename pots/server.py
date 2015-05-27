from pot import pot
import cherrypy
from cherrypy.process.plugins import Daemonizer
# add pot service in background
Daemonizer(cherrypy.engine).subscribe()



if __name__ == '__main__':

    # Mount the application
    cherrypy.tree.graft(pot, "/")

    cherrypy.server.unsubscribe()

    # Instantiate a new server object
    server = cherrypy._cpserver.Server()

    server.socket_host = "0.0.0.0"
    server.socket_port = 80
    server.thread_pool = 30

    server.subscribe()


    cherrypy.engine.start()
    cherrypy.engine.block()
