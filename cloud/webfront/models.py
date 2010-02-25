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

LARGE = "1"
THUMB = "2"
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
  photo_list = db.StringListProperty()
  representants = db.StringListProperty()

def clear_photo_store(request=None):
  logging.info('Starting to schedule the clearing of  the PhotosStore')
  for ps in PhotosStore.all():
    task = Task(url="/clear_photo/%s" % ps.key().name())
    task.add(queue_name='background-processing')
  logging.info('PhotosStore erasure scheduled')
  return HttpResponse("Cleared photo store")

def clear_photo_meta(request, photo_id):
  pm = PhotosMeta.get_by_key_name(photo_id)
  if pm != None:
    pm.delete()
  return HttpResponse("Deleted meta: %s" % photo_id)

def clear_photo(request, photo_id):
  ps = PhotosStore.get_by_key_name(photo_id)
  if ps != None:
    ps.delete()
  return HttpResponse("Deleted store: %s" % photo_id)

def clear_meta_data(request=None):
  logging.info('Starting to schedule the clearing of the PhotosMeta')
  for pm in  PhotosMeta.all():
    task = Task(url="/clear_photo_meta/%s" % pm.key().name())
    task.add(queue_name='background-processing')
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
  msg = 'Import of <a href="/tag/%s/1">tag</a> successfully scheduled, the work has started in the background.' % tag.key().name()
  logging.info(msg)
  return HttpResponse(msg)

def calculate_no_of_parts(tag_id, peerserver):
  no_of_photos = peerserver.get_photo_count_for_tag(int(tag_id))
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
    url = "/retrieve/%s/%s" % (photo_id, THUMB)
    task = Task(url=url)
    task.add(queue_name='peer-queue')
  for photo_id, _, _ in photo_list:
    url = "/retrieve/%s/%s" % (photo_id, LARGE)
    task = Task(url=url)
    task.add(queue_name='peer-queue')
  return HttpResponse(msg)

def handle_photo_list_for_tag(photo_list, tag):
  for photo in photo_list:
    pm = PhotosMeta(key_name=photo[0])
    pm.time = datetime.fromtimestamp(photo[1])
    pm.put()
    tag.photo_list.append(pm.key().name())
  tag.put() 

def load_image(photo_id, type):
  if not has_image(photo_id, type):
    retrieve_photo_from_peer(photo_id, type)
  image = PhotosStore.get_by_key_name(photo_id)
  return image

def has_image(photo_id, type):
  logging.info("has_image %s %s"  % (photo_id, type))
  image = PhotosStore.get_by_key_name(str(photo_id))
  if image == None:
    logging.info("has_image None image==None %s %s"  % (photo_id, type))
    return False
  if type == LARGE:
    logging.info("has_image type==LARGE %s %s : %s" % (photo_id, type, bool(image.jpeg)))
    return image.jpeg
  logging.info("has_image type==THUMB %s %s" % (photo_id, type))
  return image.thumb

def save_image(photo_id, jpeg, type=LARGE):
  photo = PhotosStore.get_or_insert(key_name=`photo_id`)
  photo_data = db.Blob(jpeg.data)
  if type == LARGE:
    photo.jpeg = photo_data
  else: 
    photo.thumb = photo_data
  photo_key = photo.put()
  logging.info("Stored photo %s with key %s" % (photo_id, photo_key))

def retrieve_photo_from_peer(photo_id, type):
  photo_id = int(photo_id)
  peerserver = get_my_server_proxy()
  if type == LARGE:
    dim = (800,600)
  else:
    dim = (200,150)
  jpeg  = peerserver.get_photo_object(photo_id, dim)
  save_image(photo_id, jpeg, type)

