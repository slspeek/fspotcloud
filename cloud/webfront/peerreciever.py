from google.appengine.api.labs import taskqueue
from google.appengine.ext import db
from google.appengine.api.labs.taskqueue import Task
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
from webfront.command import schedule
from webfront.util import ceil_divide
from google.appengine.runtime import DeadlineExceededError
from tracer import tracer
import logging
from webfront.models import MAX_FETCH, MAX_DELETE, LARGE, THUMB
from webfront.models import Photo, Tag, get_default_PB

def recieve_image(photo_id, jpeg, type=LARGE, tag_id=None):
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

def handle_photo_for_tag(id, time, desc, tag_id):
  logging.debug('handle_photo')
  tag = Tag.get_by_key_name(str(tag_id))
  p = Photo.get_or_insert(str(id))
  p.time = datetime.fromtimestamp(time)
  p.desc = desc
  p.put()
  tag.loaded_count += 1
  tag.put()
  if not has_image(id, THUMB):
    schedule('push_photo', map(str, [id, THUMB, tag_id]))
  if not has_image(id, LARGE):
    schedule('push_photo', map(str, [id, LARGE, tag_id]))
  else:
    tag.addPhoto(p)
  return 0

def recieve_tag(id, name, category, count):
  logging.info("Entering recieve_tag: %s %s %s %s" % (id, name, category, count))
  t = Tag.get_or_insert(str(id))
  t.name = name
  t.category_id = str(category)
  t.count = count
  t.list_loaded = False
  t.put()
  if t.import_issued:
    logging.info('schedulinh')
    schedule_image_requests_for_tag(None, id, THUMB, 0, count)
    schedule_image_requests_for_tag(None, id, LARGE, 0, count)
  return 0

def recieve_photo_data(data_string):
  logging.info('In recieve_photo_data')
  data = eval(data_string)
  for photo_data in data:
    #logging.info('In recieve_photo_data %s' % photo_data)
    save_photo(photo_data)
  return 0

def save_photo(photo_data):
  photo_id = photo_data[0]
  photo = Photo.get_or_insert(key_name=str(photo_id))
  photo.desc = photo_data[1]
  time = photo_data[2]
  photo.time = datetime.fromtimestamp(time)
  tag_list = photo_data[3]
  for tag_id in tag_list:
    #logging.info('In save_photo %s' % tag_id)
    photo.set_tag(tag_id)
  photo.put()

def recieve_photo_count(count):
  count = int(count)
  previous_count = Photo.all().count()
  need_to_load = count - previous_count 
  schedule_photo_data_requests(None, previous_count, need_to_load)
  return 0

def schedule_photo_data_requests(request, start, count):
  count_we_will_do = -1
  start, count  = int(start), int(count)
  need_to_schedule_count = ceil_divide(count, MAX_FETCH)
  if need_to_schedule_count > MAX_FETCH:
    # Schedule the next task
    next_start, next_count  = start + MAX_FETCH ** 2, count - MAX_FETCH ** 2
    url = "/task/schedule_photo_data_requests/%s/%s" % (next_start, next_count)
    task = Task(url=url)
    task.add(queue_name='background-processing')
    count_we_will_do = MAX_FETCH
  else:
    count_we_will_do = need_to_schedule_count
    
  # Do our part of the job, scheduling the head
  for i in range(0, count_we_will_do):
    beginning = start + i * MAX_FETCH
    schedule('send_photo_data', [str(beginning), str(MAX_FETCH)])
  return HttpResponse('OK')

def schedule_image_requests_for_tag(request, tag_id, type, start, count):
  tag_id = str(tag_id)
  start, count = int(start), int(count)
  all_photos_query = Photo.all().filter("tag%s =" % tag_id, True)
  image_filter = "jpeg =" if type == LARGE else "thumb ="
  if count > MAX_FETCH:
    next_start, next_count  = start + MAX_FETCH, count - MAX_FETCH
    url = "/task/schedule_image_requests_for_tag/%s/%s/%s/%s" % (tag_id,
                                                                type,
                                                                next_start,
                                                                next_count)
    task = Task(url=url)
    logging.info(url)
    task.add(queue_name='background-processing')
  # Do our part of the job, scheduling the head
  images_missing = all_photos_query.filter(image_filter, None).fetch(MAX_FETCH)
  for photo in images_missing:
    id = photo.key().name()
    schedule('push_photo', [id, type])

  return HttpResponse('OK')

  
  



