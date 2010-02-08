#!/usr/bin/env python
 
from dblayer import *
from PIL import Image
import StringIO
from xmlrpclib import Binary

def get_photo_object(id, size=(20,10)):
  id, time, uri = get_photo_row(id)
  im = Image.open(uri[6:])
  im.thumbnail(size, Image.ANTIALIAS)
  buf= StringIO.StringIO()
  im.save(buf, format= 'JPEG')
  jpeg= buf.getvalue()
  buf.close()
  print type(jpeg)
  return id, time, Binary(jpeg)


def main():
  i, time, jpeg = get_photo_object(1)
  print time
  reader = StringIO.StringIO(jpeg)
  image = Image.open(reader)
  image.show()

if __name__ == "__main__":
      main()
