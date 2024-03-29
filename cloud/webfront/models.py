from django.utils import simplejson
from google.appengine.api import memcache
from google.appengine.api.labs import taskqueue
from google.appengine.api.labs.taskqueue import Task
from appengine_django.models import BaseModel
from google.appengine.ext import db
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
from webfront.command import schedule
from webfront.util import ceil_divide
from google.appengine.runtime import DeadlineExceededError
from tracer import tracer
import logging

MAX_FETCH = 25
MAX_DELETE = 200

LARGE = "1"
THUMB = "2"

# Create your models here.
class PeerDatabase(db.Expando):
  count = db.IntegerProperty('Photo count', default=0)
  name = db.StringProperty('Name')
  max_id = db.IntegerProperty('Highest id')

def get_default_PB():
  return PeerDatabase.get_or_insert('1')

class Photo(db.Expando):
  thumb = db.BlobProperty('Thumb data')
  jpeg = db.BlobProperty('Jpeg data')
  time = db.DateTimeProperty('Photo date')
  desc = db.StringProperty('Description')

  def neighbours(this, tag):
    #photo_list = tag.photo_list
    tag_id = tag.key().name()
    photo_list = tag.photo_list
    next_photo = Photo.all().filter('tag%s =' % tag_id, True).filter('time >', this.time).fetch(1)
    if len(next_photo) > 0:
      next_photo = next_photo[0]
    else:
      next_photo = None
    if not next_photo == None:
      next = next_photo.key().name()
    else:
      next = None
    prev_photo = Photo.all().filter('tag%s =' % tag_id, True).filter('time <', this.time).fetch(1)
    if len(prev_photo) > 0:
      prev_photo = prev_photo[0]
    else:
      prev_photo = None
    if not prev_photo == None:
      prev = prev_photo.key().name()
    else:
      prev = None
    return (prev, next)


  def set_tag(this, tag_id):
    tag_id = str(tag_id)
    setattr(this, 'tag' + tag_id, True)


class Tag(BaseModel):
  category_id = db.StringProperty('Parent Tag')
  name = db.StringProperty('Name')
  count = db.IntegerProperty('Number of photos', default=0)
  color = db.StringProperty('CSS Color')
  loaded_count = db.IntegerProperty('Number of photos meta loaded', default=0)
  list_loaded = db.BooleanProperty('Photo List was loaded', default=False)
  import_issued = db.BooleanProperty('Loading of the meta data was issued', 
                                      default=False)
  photo_list = db.ListProperty(str)
  representants = db.ListProperty(db.Key)
  public = db.BooleanProperty('Visible to all the world',
                              default=False,
                              required=True)

  def photo_key_at(this, index):
    id = this.photo_list[int(index)]
    return id

  def addPhoto(this, p):
    key = p.key().name()
    if not key in this.photo_list:
      this.photo_list.append(key)
    this.put() 
    
def import_tag_data(request, tag_id):
  tag = Tag.get_by_key_name(str(tag_id))
  tag.import_issued = True
  tag.put()
  msg = '/tag_load/%s' % tag.key().name()
  logging.info(msg)
  return HttpResponseRedirect(msg)

def set_color(request, tag_id, color):
  tag = Tag.get_by_key_name(str(tag_id))
  tag.color = color
  tag.put()
  return HttpResponseRedirect('/tag_edit/%s' % tag_id)

def set_public(request, tag_id, public):
  tag = Tag.get_by_key_name(str(tag_id))
  tag.public = True if public == "1" else False
  tag.put()
  return HttpResponseRedirect("/tag")
  
def clear_all_tags(request=None):
  logging.info('Clearing all tags')
  for t in Tag.all():
    t.delete()
  msg = 'Finished clearing all tags'
  logging.info(msg)
  return HttpResponse(msg) 

def clear_all_photo_blobs(request=None):
  logging.info('Starting to schedule the clearing of the Photo blobs')
  for p in Photo.all():
    task = Task(url="/clear_photo_blobs/%s" % p.key().name())
    task.add(queue_name='background-processing')
  msg = 'Photo blobs erasure scheduled'
  logging.info(msg)
  return HttpResponse(msg)

def clear_photo_blobs(request, photo_id):
  p = Photo.get_by_key_name(photo_id)
  if p != None:
    p.jpeg = None
    p.thumb = None
  msg = 'Deleted photo blobs for: %s' % photo_id
  logging.info(msg)
  return HttpResponse(msg)

def clear_photo(request, photo_id):
  p = Photo.get_by_key_name(photo_id)
  if p != None:
    p.delete()
  return HttpResponse("Deleted photo: %s" % photo_id)


def clear_all_photo(request=None):
  try:
    for p in  Photo.all().fetch(MAX_FETCH):
      msg = "Deleted photo: %s" % p.key().name()
      p.delete()
      logging.debug(msg)
  except DeadlineExceededError:
    logging.warn("Deadline exceeded")
  finally:
    if Photo.all().count(limit=1):
      task = Task(url="/clear_all_photo")
      task.add(queue_name='background-processing')
      msg = "Scheduled subsequend delete task"
    else:
      msg = "All photos deleted"
  logging.info(msg)
  return HttpResponse(msg)

def import_tags(request):
  schedule('push_tags', [])
  return HttpResponse('The tags import is given to control')

""" @tracer """
def load_image(photo_id, type):
  if not has_image(photo_id, type):
    schedule('push_photo', [photo_id, type])
  photo = memcache.get(photo_id)
  if photo == None:
    photo = Photo.get_by_key_name(photo_id)
    memcache.set(photo_id, photo, 60)
  return photo

def has_image(photo_id, type):
  photo = Photo.get_by_key_name(str(photo_id))
  if photo == None:
    return False
  if type == LARGE:
    return bool(photo.jpeg)
  return bool(photo.thumb)

def ajax_get_tag_progress(request):
  from google.appengine.api import users
  user = users.get_current_user()
  xhr = request.GET.has_key('xhr')
  response_dict = {}
  tag_id = request.GET.get('tag_id', '36')
  tag = Tag.get_by_key_name(str(tag_id))
  progress = (len(tag.photo_list)/float(tag.count))*75 
  progress += (tag.loaded_count/float(tag.count))*25
  response_dict.update({'progress': progress})
  response_dict.update({'tag_id': tag_id})
  logging.debug("ajax for tag: %s at %s user: %s" % (tag_id, progress, user));
  return HttpResponse(simplejson.dumps(response_dict),
                      mimetype='application/javascript')

def ajax_photo_at(request):
  response_dict = {}
  tag_id = request.GET.get('tag_id', '36')
  index = request.GET.get('index', '0')
  logging.debug("ajax for photo at  %s at %s" % (tag_id, index));
  tag = Tag.get_by_key_name(str(tag_id))
  if int(index) < len(tag.photo_list):
    photo_id = tag.photo_key_at(index)
    response_dict.update({'photo_id': photo_id})
  else:
    response_dict.update({'photo_id': 'not found', 'error': 1})
  return HttpResponse(simplejson.dumps(response_dict),
                      mimetype='application/javascript')
