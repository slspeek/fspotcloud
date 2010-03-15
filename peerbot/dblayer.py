#!/usr/bin/env python

from pysqlite2 import dbapi2 as sqlite
from PIL import Image
import StringIO
from xmlrpclib import Binary

connection = sqlite.connect('photos.db')

def get_photo_row(id):
  cursor = connection.cursor()
  id = str(id)
  cursor.execute('SELECT id, time, uri FROM photos WHERE id=? ORDER BY time ', (id,))
  row = cursor.fetchone()
  return tuple(row)

def get_tag_list(parent_id=None):
  cursor = connection.cursor()
  tag_list = []
  cursor.execute('SELECT id, name, category_id FROM tags ORDER BY id')
  for row in cursor:
    tag_id = row[0]
    photo_count = get_photo_count_for_tag(tag_id)
    tag_list.append((row[0], row[1], row[2], photo_count))
  return tag_list

def get_photo_list_for_tag(tag_id, offset=0, limit=10):
  print 'TagId', tag_id, type(tag_id)
  cursor = connection.cursor()
  photo_list = []
  cursor.execute('SELECT photos.id, photos.time, photos.description, photo_tags.tag_id FROM photo_tags, photos WHERE tag_id=? AND photos.id=photo_tags.photo_id ORDER BY photos.time LIMIT ? OFFSET ?',
                map(str,(tag_id,limit,offset)))
  for row in cursor:
    photo_list.append([str(row[0]), row[1], row[2], str(row[3])])
  #print photo_list
  return photo_list

def get_photo_count_for_tag(tag_id):
  cursor = connection.cursor()
  cursor.execute('SELECT COUNT(photos.id) FROM photo_tags, photos WHERE tag_id=? AND photos.id=photo_tags.photo_id ', (str(tag_id),))
  row = cursor.fetchone()
  return row[0]

def get_photo_object(id, size=(20,10)):
  id, time, uri = get_photo_row(id)
  im = Image.open(uri[6:])
  im.thumbnail(size, Image.ANTIALIAS)
  buf= StringIO.StringIO()
  im.save(buf, format= 'JPEG')
  jpeg= buf.getvalue()
  buf.close()
  return Binary(jpeg)
 
def main():
  print get_photo_row(5713)
  print get_tag_list()
  print get_photo_list_for_tag(2)
  print get_photo_list_for_tag(51)
  jpeg = get_photo_object(5713, (400,300))
  reader = StringIO.StringIO(jpeg)
  image = Image.open(reader)
  image.show()

if __name__ == "__main__":
      main()
