import xmlrpclib
import dblayer
from config import SERVER_URL, BIG_DIM, THUMB_DIM

s = xmlrpclib.ServerProxy(SERVER_URL)

def send_photo_count():
  print 'Send photo count'
  count = dblayer.get_photo_count()
  s.recieve_photo_count(count)

def send_photo_data(offset, limit):
  print 'Send photo data'
  photo_list = dblayer.get_photo_list(offset, limit)
  s.recieve_photo_data(str(photo_list))

def push_tag_data(id, offset, limit):
  photo_list = dblayer.get_photo_list_for_tag(id, offset, limit)
  for photo in photo_list:
    s.handle_photo_for_tag(*photo)

def push_photo(id, type):
  dim = THUMB_DIM if type == "2" else BIG_DIM
  jpeg = dblayer.get_photo_object(id, dim)
  print s.recieve_image(int(id), jpeg, type)

def push_tags():
  for tag in dblayer.get_tag_list():
    s.recieve_tag(*tag)

def main():
  pass

if __name__ == '__main__':
  main()
