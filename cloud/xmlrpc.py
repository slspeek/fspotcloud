from GAEXMLRPCTransport import GAEXMLRPCTransport
import xmlrpclib

def get_server_proxy(host_url):
  rpc_server = xmlrpclib.ServerProxy(host_url,
               GAEXMLRPCTransport())
  return rpc_server
