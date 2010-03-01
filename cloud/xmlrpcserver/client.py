import xmlrpclib
s = xmlrpclib.ServerProxy('http://fspotcloud.appspot.com/xmlrpc/')
print s.app.getName()
