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
import logging

MAX_FETCH = 50
MAX_DELETE = 200

LARGE = "1"
THUMB = "2"

# Create your models here.
class Photo(BaseModel):
  thumb = db.BlobProperty('Thumb data')
  jpeg = db.BlobProperty('Jpeg data')
  time = db.DateTimeProperty('Photo date')
  desc = db.StringProperty('Description')

  def neighbours(this, tag):
    photo_list = tag.photo_list
    key_name = this.key().name()
    index = photo_list.index(key_name)
    if index < len(photo_list) - 1: # we have a next
      next = photo_list[index + 1]
    else:
      next = None
    if index > 0:
      prev = photo_list[index - 1]
    else:
      prev = None
    return (prev, next)

class Tag(BaseModel):
  category_id = db.StringProperty('Parent Tag')
  name = db.StringProperty('Name')
  count = db.IntegerProperty('Number of photos', default=0)
  loaded_count = db.IntegerProperty('Number of photos loaded', default=0)
  list_loaded = db.BooleanProperty('Photo List was loaded', default=False)
  import_issued = db.BooleanProperty('Loading of the meta data was issued', 
                                      default=False)
  photo_list = db.ListProperty(str)
  representants = db.ListProperty(db.Key)
  public = db.BooleanProperty('Visible to all the world',
                              default=False,
                              required=True)

  def addPhoto(this, p):
    key = p.key().name()
    if not key in this.photo_list:
      this.photo_list.append(key)
    this.put() 
    

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
    for p in  Photo.all().fetch(MAX_DELETE):
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

def save_tag(id, name, category, count):
  logging.info("Entering save_tag: %s %s %s" % (id, name, category))
  t = Tag.get_or_insert(str(id))
  t.name = name
  t.category_id = str(category)
  t.count = count
  t.list_loaded = False
  t.put()
  return 0

def import_tag_data(request, tag_id):
  tag = Tag.get_by_key_name(str(tag_id))
  part_count = calculate_part_count(tag)
  for part in range(0, part_count):
    offset = part * MAX_FETCH
    limit = MAX_FETCH
    schedule('push_tag_data', map(str,[tag_id, offset, limit]))
  tag.import_issued = True
  tag.put()
  msg = 'Import of <a href="/tag/%s/1">tag</a> successfully scheduled in control' % tag.key().name()
  logging.info(msg)
  return HttpResponse(msg)

def calculate_part_count(tag):
  no_of_parts = ceil_divide(tag.count, MAX_FETCH)
  return no_of_parts

def handle_photo_for_tag(id, time, desc, tag_id):
  logging.debug('handle_photo')
  tag = Tag.get_by_key_name(str(tag_id))
  p = Photo.get_or_insert(str(id))
  p.time = datetime.fromtimestamp(time)
  p.desc = desc
  p.put()
  if not has_image(id, THUMB):
    schedule('push_photo', map(str, [id, THUMB, tag_id]))
  if not has_image(id, LARGE):
    schedule('push_photo', map(str, [id, LARGE, tag_id]))
  else:
    tag.addPhoto(p)
  return 0

def load_image(photo_id, type):
  if not has_image(photo_id, type):
    schedule('push_photo', [photo_id, type, tag_id])
  image = memcache.get(photo_id)
  if image == None:
    image = Photo.get_by_key_name(photo_id)
    memcache.set(photo_id, image, 60)
  return image

def has_image(photo_id, type):
  image = Photo.get_by_key_name(str(photo_id))
  if image == None:
    return False
  if type == LARGE:
    return bool(image.jpeg)
  return bool(image.thumb)

def save_image(photo_id, jpeg, type=LARGE, tag_id=None):
  photo = Photo.get_or_insert(key_name=str(photo_id))
  photo_data = db.Blob(jpeg.data)
  if type == LARGE:
    tag = Tag.get_by_key_name(str(tag_id)) 
    photo.jpeg = photo_data
    tag.addPhoto(photo)
  else: 
    photo.thumb = photo_data
  photo_key = photo.put()
  logging.info("Stored photo %s with key %s of type %s" % (photo_id, photo_key, type))
  return 0

def ajax_get_tag_progress(request):
  xhr = request.GET.has_key('xhr')
  response_dict = {}
  tag_id = request.GET.get('tag_id', '36')
  tag = Tag.get_by_key_name(str(tag_id))
  progress = (len(tag.photo_list)/float(tag.count))*100
  response_dict.update({'progress': progress})
  response_dict.update({'tag_id': tag_id})
  logging.info("ajax for tag: %s" % tag_id);
  return HttpResponse(simplejson.dumps(response_dict),
                      mimetype='application/javascript')
