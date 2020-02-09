import cherrypy
import cherrypy_cors
import json
import logging
import random
import os
import logging.config
import traceback
from apps.routerequest.routerequest import routeRequest


class host(object):

    @cherrypy.expose
    def index(self):
        rslt = ""
        try:
            if cherrypy.request.method == 'OPTIONS':
            # This is a request that browser sends in CORS prior to
            # sending a real request.

            # Set up extra headers for a pre-flight OPTIONS request.
                cherrypy_cors.preflight(allowed_methods=['GET', 'POST'])

            if cherrypy.request.method == 'POST':
                print("reach server")
                header = cherrypy.request.headers
                rawData = cherrypy.request.body.read(int(cherrypy.request.headers['Content-Length'])).decode('utf-8')
                body = json.loads(rawData)
                #function call to route the header
                userid = body["datahdr"]["userid"]
                logging.config.fileConfig("loggers.conf", defaults={'logfilename':userid}, disable_existing_loggers=False)
                               
                rslt = json.dumps(routeRequest(body,header))
                #rslt = json.dumps({"name":"vignesh"})
                logging.debug(rslt)
                #rslt="take it"
            else:
                rslt="Method not allowed"
        except:
            rslt = "Excetion occurs"
            print("Exception occurs") 
            traceback.print_exc()
        return rslt


def main():
    cherrypy.config.update({'server.socket_host': "localhost", 'server.socket_port': 8001,'cors.expose.on': True,})
    cherrypy.tree.mount(host(),'/')
    cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
    #cherrypy.response.headers[ "Content-Type"] = "application/json"
    cherrypy.response.headers["Access-Control-Allow-Methods"] = "GET, POST, HEAD, PUT, DELETE"
    allow_headers = ["Cache-Control", "X-Proxy-Authorization", "X-Requested-With", "Content-Type"]
    cherrypy.response.headers["Access-Control-Allow-Headers"] = ",".join(allow_headers)
    cherrypy_cors.install()
    cherrypy.engine.start()
    cherrypy.engine.block()


class myFileHandler(logging.FileHandler):
    def __init__(self, path, filename, mode):
        path = path + "/" + filename
        try:
            os.mkdir(path)
        except:
            print("log file exsists")
        super(myFileHandler, self).__init__(path+"/"+"server.log", mode)


if  __name__ == "__main__":
    main()