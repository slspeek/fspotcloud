#!/usr/bin/env python
 
import xmlrpclib
import StringIO
from PIL import Image

s = xmlrpclib.ServerProxy('http://localhost:8000')

id, time, jpeg =  s.get_photo_object(3, (300,200))
reader = StringIO.StringIO(jpeg)
image = Image.open(reader)
image.show()
