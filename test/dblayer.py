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
  pass
 
def main():
  print get_photo_row(2455)

if __name__ == "__main__":
      main()
