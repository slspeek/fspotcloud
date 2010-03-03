#!/usr/bin/env python

from dblayer import get_tag_list, get_photo_list_for_tag, get_photo_object, get_photo_count_for_tag
from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
  rpc_paths = ('/RPC2',)

def ping():
  return 'Up'

# Create server
server = SimpleXMLRPCServer(("0.0.0.0", 80),
              requestHandler=RequestHandler)
server.register_function(get_photo_object)
server.register_function(get_tag_list)
server.register_function(get_photo_list_for_tag)
server.register_function(get_photo_count_for_tag)
server.register_function(ping)
server.serve_forever()

