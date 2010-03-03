import xmlrpclib
import dblayer
#s = xmlrpclib.ServerProxy('http://fspotcloud.appspot.com/xmlrpc/')
s = xmlrpclib.ServerProxy('http://localhost:8000/xmlrpc/')
id = 5012
jpeg = dblayer.get_photo_object(id, (1200, 1000))
print s.save_image(id, jpeg, "1")
print s.get_command()
