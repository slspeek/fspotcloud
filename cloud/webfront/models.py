from google.appengine.api.labs import taskqueue
from google.appengine.api.labs.taskqueue import Task
from appengine_django.models import BaseModel
from django.shortcuts import render_to_response
from django.http import HttpResponse
from google.appengine.ext import db
from xmlrpc import get_my_server_proxy
from datetime import datetime
from StringIO import StringIO
import logging

# Create your models here.
class PhotosStore(BaseModel):
  id = db.IntegerProperty('F-Spot ID')
  thumb = db.BlobProperty('Thumb data')
  jpeg = db.BlobProperty('Jpeg data')

class PhotosMeta(BaseModel):
  id = db.IntegerProperty('F-Spot ID')
  time = db.DateTimeProperty('Photo date')
  #peerdb = db.ReferenceProperty(db.PeerDatabases)
 
class Settings(BaseModel):
  pass

class State(BaseModel):
  var = db.StringProperty('Variable')
  value = db.StringProperty('Value')

class PeerDatabases(BaseModel):
  id = db.IntegerProperty('Peer Database ID')
  desc = db.StringProperty('Description')
  uri = db.StringProperty('Peer Server URI')

class Tags(BaseModel):
  id = db.IntegerProperty('Tag ID')
  category_id = db.IntegerProperty('Parent Tag')
  name = db.StringProperty('Name')
  list_loaded = db.BooleanProperty('Photo List was loaded')
  #peerdb = db.ReferenceProperty(db.PeerDatabases)
  photo_list = db.ListProperty(int)
  representants = db.ListProperty(int)

def clear_photo_store(request=None):
  logging.info('Starting to clear the PhotosStore')
  for ps in PhotosStore.all():
    ps.delete()
  logging.info('PhotosStore cleared')
  return HttpResponse("Cleared photo store")

def clear_meta_data(request=None):
  logging.info('Starting to clear the PhotosMeta')
  for pm in  PhotosMeta.all():
    pm.delete()
  logging.info('PhotosMeta cleared')
  logging.info('Starting to clear the Tags')
  for tag in Tags.all():
    tag.delete()
  logging.info('Tags cleared')
  return HttpResponse("Meta data cleared")

def import_tags(request):
  clear_meta_data()
  peerserver = get_my_server_proxy()
  tag_list = peerserver.get_tag_list()
  for tag in tag_list:
    t = Tags()
    t.id = int(tag[0])
    t.name = tag[1]
    t.category_id = int(tag[2])  
    t.list_loaded = False
    t.put()
  return HttpResponse('The tags were imported')

def load_tag_by_id(tag_id):
  tag = Tags.gql('WHERE id = :1', tag_id).fetch(1)[0]
  return tag

def import_tag_data(request=None, tag_id="51"):
  tag_id = int(tag_id)
  tag = load_tag_by_id(tag_id)
  peerserver = get_my_server_proxy()
  photo_list = peerserver.get_photo_list_for_tag(tag_id)
  for photo in photo_list:
    pm = PhotosMeta()
    pm.id = int(photo[0])
    pm.time = datetime.fromtimestamp(photo[1])
    pm.put()
    logging.debug("PhotosMeta stored %s" % pm.id)
    tag.photo_list.append(pm.id)
  tag.list_loaded = True
  tag.put()
# Set out Tasks for retrieving the images slowly
  for photo_id in tag.photo_list:
    url = "/retrieve/%s" % photo_id
    task = Task(url=url)
    task.add(queue_name='peer-queue')
  return HttpResponse('Import <a href="/tag/%s">tag</a> successfully' % tag_id)


def load_image(photo_id):
  image = None
  if not has_image(photo_id):
    retrieve_photo_from_peer(photo_id)
  image = get_image_by_id(photo_id)
  return image

def get_image_by_id(photo_id):
  image = PhotosStore.gql("WHERE id = :1", photo_id).fetch(1)[0]
  return image

def has_image(photo_id):
  count = PhotosStore.gql("WHERE id = :1", photo_id).count()
  return count > 0 
  
def save_image(photo_id, jpeg):
  photo = PhotosStore()
  photo.id = photo_id
  photo.jpeg = db.Blob(jpeg.data)
  photo_key = photo.put()
  logging.info("Stored photo %s with key %s" % (photo_id, photo_key))
  return photo.id

def retrieve_photo_from_peer(photo_id):
  photo_id = int(photo_id)
  peerserver = get_my_server_proxy()
  jpeg  = peerserver.get_photo_object(photo_id, (200,150))
  save_image(photo_id, jpeg)

