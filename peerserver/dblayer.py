#!/usr/bin/env python

from pysqlite2 import dbapi2 as sqlite
from PIL import Image
import StringIO
from xmlrpclib import Binary

connection = sqlite.connect('photos.db')
cursor = connection.cursor()

def get_photo_row(id):
  id = `id`
  cursor.execute('SELECT id, time, uri FROM photos WHERE id=? ORDER BY time ', (id,))
  row = cursor.fetchone()
  return row[0], row[1], row[2]

def get_tag_list(parent_id=None):
  print "Called"
  tag_list = []
  cursor.execute('SELECT id, name, category_id FROM tags ORDER BY id')
  for row in cursor:
    tag_list.append((row[0], row[1], row[2]))
  return tag_list

def get_photo_list_for_tag(tag_id):
  photo_list = []
  cursor.execute('SELECT photos.id, photos.time, photo_tags.tag_id FROM photo_tags, photos WHERE tag_id=? AND photos.id=photo_tags.photo_id ', (`tag_id`,))
  for row in cursor:
    photo_list.append((row[0], row[1], row[2]))
  return photo_list

def get_photo_object(id, size=(20,10)):
  id, time, uri = get_photo_row(id)
  im = Image.open(uri[6:])
  im.thumbnail(size, Image.ANTIALIAS)
  buf= StringIO.StringIO()
  im.save(buf, format= 'JPEG')
  jpeg= buf.getvalue()
  buf.close()
  return Binary(jpeg)

if __name__ == "__main__":
      main()
 
def main():
  print get_photo_row(2455)
  print get_tag_list()
  print get_photo_list_for_tag(2)
  print get_photo_list_for_tag(51)
  i, time, jpeg = get_photo_object(1)
  print time
  reader = StringIO.StringIO(jpeg)
  image = Image.open(reader)
  image.show()

if __name__ == "__main__":
      main()