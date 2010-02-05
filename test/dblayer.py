#!/usr/bin/env python

from pysqlite2 import dbapi2 as sqlite

connection = sqlite.connect('photos.db')

cursor = connection.cursor()


def get_first_id():
  cursor.execute('SELECT id, time FROM photos ORDER BY time LIMIT 1 OFFSET 0')
  row = cursor.fetchall()[0]
  return row[0]
 
def main():
  print get_first_id()

if __name__ == "__main__":
      main()
