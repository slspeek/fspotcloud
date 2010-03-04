from django.http import HttpResponse
from django.shortcuts import render_to_response
from webfront.models import *
import logging
from google.appengine.ext import db
from webfront.bigvar import get_value
from webfront.util import ceil_divide

NUMBER_OF_COLUMNS = 3
NUMBER_OF_ROWS = 3
NUMBER_OF_PHOTOS = NUMBER_OF_COLUMNS * NUMBER_OF_ROWS

def ping_page(request):
  if False:
    msg = "Peerbot is up"
  else:
    msg = "Peerbot is down"
  return HttpResponse(msg)

def get_image(request, pic_id, type):
  response = HttpResponse(content_type='image/jpeg')
  image = load_image(pic_id, type)
  if type == LARGE:
    image_data = image.jpeg
  else:
    image_data = image.thumb
  response.write(image_data)
  logging.info("Served image %s of type %s" % (image.key().name(),
                                                type))
  return response

def tag_index(request):
  tag_list = Tag.all().order('name')
  tags = []
  for t in tag_list:
    tags.append((t.key().name(), t.name, t.import_issued))
  peer_up = get_value('peer_up')
  if peer_up == 'False':
    peer_up = []
  return render_to_response('tag_index.html', 
                            { 'tags': tags,
                              'peer_up': peer_up })
  
def tag_page(request, tag_id, page_id):
  page_id = int(page_id)
  tag = Tag.get_by_key_name(tag_id)
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
  return render_to_response('tag.html', 
                            {'pics': table,
                            'name': tag.name,
                            'pages': page_list,
                            'tag_id': tag_id,
                            'page_id': page_id })
 
def get_pages(tag):
  no_of_photos = len(tag.photo_list)
  no_of_pages = ceil_divide(no_of_photos, NUMBER_OF_PHOTOS)
  page_list = []
  for page_id in range(0, no_of_pages-1):
    start = page_id * NUMBER_OF_PHOTOS + 1
    end = start + NUMBER_OF_PHOTOS - 1
    """ Normal case """
    page_list.append(("%s - %s" % (start, end), 
                      "/tag/%s/%s" % (tag.key().name(), page_id + 1)))
  """ Last case """
  start = (no_of_pages - 1) * NUMBER_OF_PHOTOS + 1
  end = no_of_photos
  page_list.append(("%s - %s" % (start, end),
                    "/tag/%s/%s" % (tag.key().name(), no_of_pages)))
  return page_list

def photo_page(request, tag_id, page_id, photo_id):
  tag = Tag.get_by_key_name(tag_id)
  source = "/tag/%s/%s" % (tag_id, page_id)
  return render_to_response('photo.html',
                      {'image': photo_id,
                       'name': tag.name,
                       'source': source })
  
