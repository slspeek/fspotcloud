from GAEXMLRPCTransport import GAEXMLRPCTransport
import xmlrpclib

def get_server_proxy(host_url):
  rpc_server = xmlrpclib.ServerProxy(host_url,
               GAEXMLRPCTransport())
  return rpc_server


def get_my_server_proxy():
  return get_server_proxy("http://speek.xs4all.nl")


