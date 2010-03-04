import xmlrpclib
import dblayer
from config import SERVER_URL, BIG_DIM, THUMB_DIM

s = xmlrpclib.ServerProxy(SERVER_URL)

def push_tag_data(id, offset, limit):
  photo_list = dblayer.get_photo_list_for_tag(id, offset, limit)
  for photo in photo_list:
    s.handle_photo_for_tag(*photo)

def push_photo(id, type):
  if not s.has_image(int(id), type):
    dim = THUMB_DIM if type == "2" else BIG_DIM
    jpeg = dblayer.get_photo_object(id, dim)
    print s.save_image(int(id), jpeg, type)

def push_tag(tag_id, type):
  for id, _, _, _ in dblayer.get_photo_list_for_tag(tag_id, limit=1000):
    print id
    push_photo(id, type)

def push_tags():
  for tag in dblayer.get_tag_list():
    s.save_tag(*tag)

def main():
  test
  push_tag(59, "2")
  push_tag(59, "1")

if __name__ == '__main__':
  main()
