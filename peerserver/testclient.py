#!/usr/bin/env python
 
import sys
import xmlrpclib
import StringIO
from PIL import Image

s = xmlrpclib.ServerProxy('http://localhost')
id = int(sys.argv[1])
resolution = int(sys.argv[2]), int(sys.argv[3])
print id, resolution
_, time, jpeg =  s.get_photo_object(id, resolution)
reader = StringIO.StringIO(jpeg)
image = Image.open(reader)
image.show()
tag_list = s.get_tag_list()
print tag_list
photo_list = s.get_photo_list_for_tag(51)
print photo_list
