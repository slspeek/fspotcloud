#!/usr/bin/env python

from pysqlite2 import dbapi2 as sqlite

connection = sqlite.connect('photos.db')

cursor = connection.cursor()


def get_photo_row(id):
  id = `id`
  cursor.execute('SELECT id, time, uri FROM photos WHERE id=? ORDER BY time ', (id,))
  row = cursor.fetchone()
  return row[0], row[1], row[2]

def get_tag_list(parent_id=None):
  tag_list = []
  cursor.execute('SELECT id, name, category_id FROM tags ORDER BY id')
  for row in cursor:
    tag_list.append((row[0], row[1], row[2]))
  return tag_list

def get_photo_list_for_tag(tag_id):
  photo_list = []
  cursor.execute('SELECT photo_id, tag_id FROM photo_tags WHERE tag_id=? ', (`tag_id`,))
  for row in cursor:
    photo_list.append((row[0], row[1]))
  return photo_list


 
def main():
  print get_photo_row(2455)
  print get_tag_list()
  print get_photo_list_for_tag(2)
  print get_photo_list_for_tag(51)

if __name__ == "__main__":
      main()
