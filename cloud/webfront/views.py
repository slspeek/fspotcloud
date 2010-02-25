from django.http import HttpResponse
from django.shortcuts import render_to_response
from webfront.models import *
import logging
from google.appengine.ext import db
from xmlrpc import ping
import xmlrpc
from webfront.bigvar import get_value

NUMBER_OF_COLUMNS = 4
NUMBER_OF_ROWS = 4
NUMBER_OF_PHOTOS = NUMBER_OF_COLUMNS * NUMBER_OF_ROWS

def index(request):
  photo_list = PhotosStore.all().order('id')
  return render_to_response('index.html', {'photo_list': photo_list})

def ping_page(request):
  if ping():
    msg = "Peerserver is up"
  else:
    msg = "Peerserver is down"
  return HttpResponse(msg)

def get_image(request, pic_id):
  response = HttpResponse(content_type='image/jpeg')
  image = load_image(pic_id)
  response.write(image.jpeg)
  logging.info("Served image %s" % image.key().name())
  return response

def tag_index(request):
  tag_list = Tags.all().order('name')
  tags = []
  for t in tag_list:
    tags.append((t.key().name(), t.name, t.list_loaded))
  peer_up = get_value('peer_up')
  if peer_up == 'False':
    peer_up = []
  return render_to_response('tag_index.html', { 'tags': tags, 'peer_up': peer_up })

  
def tag_page(request, tag_id, page_id):
  page_id = int(page_id)
  tag = Tags.get_by_key_name(tag_id)
  start = (page_id - 1) * NUMBER_OF_PHOTOS
  end = start + NUMBER_OF_PHOTOS
  logging.info("Slicing from %s to %s" % (start, end))
  photos = tag.photo_list[start:end]
  table = []
  cnt = 0
  for pic_id in photos:
    if cnt % NUMBER_OF_COLUMNS == 0:
      row = []
      table.append(row)
    row.append(pic_id)
    cnt += 1
  page_list = get_pages(tag)
  return render_to_response('tag.html', {'pics': table,  'name': tag.name, 'pages': page_list })
 
def get_pages(tag):
  no_of_photos = len(tag.photo_list)
  no_of_pages = no_of_photos // NUMBER_OF_PHOTOS 
  if not no_of_photos % NUMBER_OF_PHOTOS == 0:
    no_of_pages += 1
  page_list = []
  for page_id in range(0, no_of_pages-1):
    start = page_id * NUMBER_OF_PHOTOS + 1
    end = start + NUMBER_OF_PHOTOS - 1
    page_list.append(("%s - %s" % (start, end), "/tag/%s/%s" % (tag.key().name(), page_id + 1)))
  start = (no_of_pages - 1) * NUMBER_OF_PHOTOS + 1
  end = no_of_photos
  page_list.append(("%s - %s" % (start, end), "/tag/%s/%s" % (tag.key().name(), no_of_pages)))
  return page_list

