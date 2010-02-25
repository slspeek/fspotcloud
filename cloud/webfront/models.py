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

MAX_FETCH = 50

# Create your models here.
class PhotosStore(BaseModel):
  thumb = db.BlobProperty('Thumb data')
  jpeg = db.BlobProperty('Jpeg data')

class PhotosMeta(BaseModel):
  time = db.DateTimeProperty('Photo date')
 
class Settings(BaseModel):
  pass

class State(BaseModel):
  value = db.StringProperty('Value')

class PeerDatabases(BaseModel):
  desc = db.StringProperty('Description')
  uri = db.StringProperty('Peer Server URI')

class Tags(BaseModel):
  category_id = db.StringProperty('Parent Tag')
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
    key_name = tag[0]
    t = Tags(key_name=key_name)
    t.name = tag[1]
    t.category_id = tag[2]  
    t.list_loaded = False
    t.put()
  return HttpResponse('The tags were imported')

def import_tag_data(request=None, tag_id="51"):
  tag_id = int(tag_id)
  tag = Tags.get_by_key_name(tag_id)
  peerserver = get_my_server_proxy()
  no_of_parts = calculate_no_of_parts(tag_id, peerserver)
  for part in range(0, no_of_parts):
    offset = part * MAX_FETCH
    limit = MAX_FETCH
    url = "/import_tag/%s/%s/%s" % (tag_id, offset, limit)
    task = Task(url=url)
    task.add(queue_name='peer-queue')
  tag.list_loaded = True
  tag.put()
  return HttpResponse('Import <a href="/tag/%s/1">tag</a> successfully' % tag_id)

def calculate_no_of_parts(tag_id, peerserver):
  no_of_photos = peerserver.get_photo_count_for_tag(tag_id)
  no_of_parts = no_of_photos // MAX_FETCH
  if not no_of_photos % MAX_FETCH == 0:
    no_of_parts += 1
  return no_of_parts


def import_tag_data_part(request, tag_id, offset, limit):
  offset = int(offset)
  limit = int(limit)
  tag = Tags.get_by_key_name(tag_id)
  tag_id = int(tag_id)
  peerserver = get_my_server_proxy()
  photo_list = peerserver.get_photo_list_for_tag(tag_id, offset, limit)
  handle_photo_list_for_tag(photo_list, tag)
  msg = "import tag data %s offset %s limit %s succeeded" % (tag_id, offset, limit)
  logging.info(msg)
# Set out Tasks for retrieving the images slowly
  for photo_id, _, _ in photo_list:
    url = "/retrieve/%s" % photo_id
    task = Task(url=url)
    task.add(queue_name='peer-queue')
  return HttpResponse(msg)

def handle_photo_list_for_tag(photo_list, tag):
  for photo in photo_list:
    pm = PhotosMeta(key_name=photo[0])
    pm.time = datetime.fromtimestamp(photo[1])
    pm.put()
    logging.debug("PhotosMeta stored %s" % pm.id)
    tag.photo_list.append(pm.id)
  tag.put() 

def load_image(photo_id):
  image = None
  if not has_image(photo_id):
    retrieve_photo_from_peer(photo_id)
  image = PhotoStore.get_by_key_name(photo_id)
  return image

def has_image(photo_id):
  image = PhotosStore.get_by_key_name(photo_id)
  return image != None

def save_image(photo_id, jpeg):
  photo = PhotosStore(key_name=photo_id)
  photo.jpeg = db.Blob(jpeg.data)
  photo_key = photo.put()
  logging.info("Stored photo %s with key %s" % (photo_id, photo_key))
  return photo.id

def retrieve_photo_from_peer(photo_id):
  photo_id = int(photo_id)
  peerserver = get_my_server_proxy()
  jpeg  = peerserver.get_photo_object(photo_id, (200,150))
  save_image(photo_id, jpeg)

