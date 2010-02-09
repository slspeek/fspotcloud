#!/usr/bin/env python

from objectlayer import get_photo_object
from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
  rpc_paths = ('/RPC2',)

# Create server
server = SimpleXMLRPCServer(("0.0.0.0", 8000),
              requestHandler=RequestHandler)
server.register_function(get_photo_object)
server.serve_forever()

