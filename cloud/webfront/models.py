from google.appengine.api.labs import taskqueue
from google.appengine.api.labs.taskqueue import Task
from appengine_django.models import BaseModel
from google.appengine.ext import db
from django.http import HttpResponse
from datetime import datetime
from webfront.command import schedule
from webfront.util import ceil_divide
import logging

MAX_FETCH = 50

LARGE = "1"
THUMB = "2"

# Create your models here.
class Photo(BaseModel):
  thumb = db.BlobProperty('Thumb data')
  jpeg = db.BlobProperty('Jpeg data')
  time = db.DateTimeProperty('Photo date')
  desc = db.StringProperty('Description')

class Tag(BaseModel):
  category_id = db.StringProperty('Parent Tag')
  name = db.StringProperty('Name')
  count = db.IntegerProperty('Number of photos')
  list_loaded = db.BooleanProperty('Photo List was loaded')
  import_issued = db.BooleanProperty('Loading of the meta data was issued')
  photo_list = db.ListProperty(str)
  representants = db.ListProperty(db.Key)

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
  logging.info('Starting to schedule the clearing of the Photo')
  for p in  Photo.all():
    task = Task(url="/clear_photo/%s" % p.key().name())
    task.add(queue_name='background-processing')
  logging.info('Photo cleared')
  logging.info('Starting to clear the Tag')
  for tag in Tag.all():
    tag.delete()
  logging.info('Tag cleared')
  return HttpResponse("Meta data cleared")

def import_tags(request):
  schedule('push_tags', [])
  return HttpResponse('The tags import is given to C&amp;C')

def save_tag(id, name, category, count):
  logging.info("Entering save_tag: %s %s %s" % (id, name, category))
  t = Tag(key_name=str(id))
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
  schedule('push_tag', [str(tag_id), "2"])
  schedule('push_tag', [str(tag_id), "1"])
  return HttpResponse(msg)

def calculate_part_count(tag):
  no_of_parts = ceil_divide(tag.count, MAX_FETCH)
  return no_of_parts

def handle_photo_for_tag(id, time, desc, tag_id):
  logging.info('handle_phtoto')
  tag = Tag.get_by_key_name(str(tag_id))
  p = Photo.get_or_insert(str(id))
  p.time = datetime.fromtimestamp(time)
  p.desc = desc
  p.put()
  tag.photo_list.append(p.key().name())
  tag.put() 
  return 0

def load_image(photo_id, type):
  if not has_image(photo_id, type):
    schedule('push_photo', [photo_id, type])
  image = Photo.get_by_key_name(photo_id)
  return image

def has_image(photo_id, type):
  logging.info('Entering has_image')
  image = Photo.get_by_key_name(str(photo_id))
  logging.info('has_image')
  if image == None:
    return False
  if type == LARGE:
    return bool(image.jpeg)
  return bool(image.thumb)

def save_image(photo_id, jpeg, type=LARGE):
  photo = Photo.get_or_insert(key_name=str(photo_id))
  photo_data = db.Blob(jpeg.data)
  if type == LARGE:
    photo.jpeg = photo_data
  else: 
    photo.thumb = photo_data
  photo_key = photo.put()
  logging.info("Stored photo %s with key %s of type %s" % (photo_id, photo_key, type))
  return 0

