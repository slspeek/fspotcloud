import xmlrpclib
import dblayer

SERVER_URL='http://localhost:8000/xmlrpc/'
s = xmlrpclib.ServerProxy(SERVER_URL)

def push_tag(tag_id, type):
  for id, _, _ in dblayer.get_photo_list_for_tag(tag_id, limit=1000):
    print id
    dim = (200,150) if type == "2" else (1200,1000)
    jpeg = dblayer.get_photo_object(id, dim)
    id = int(id)
    if not s.has_image(id, type):
      print s.save_image(int(id), jpeg, type)

def push_tags():
  for tag in dblayer.get_tag_list():
    s.save_tag(*tag)

def main():
  push_tag(59, "2")
  push_tag(59, "1")

if __name__ == '__main__':
  main()
