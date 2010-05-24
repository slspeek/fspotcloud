from django.http import HttpResponse
from django.shortcuts import render_to_response
from webfront.models import *
import logging
from google.appengine.ext import db
from webfront.bigvar import get_value
from webfront.util import ceil_divide
from tracer import tracer

NUMBER_OF_COLUMNS = 3
NUMBER_OF_ROWS = 3
NUMBER_OF_PHOTOS = NUMBER_OF_COLUMNS * NUMBER_OF_ROWS

def ping_page(request):
  if False:
    msg = "Peerbot is up"
  else:
    msg = "Peerbot is down"
  return HttpResponse(msg)

@tracer
def get_image(request, pic_id, type):
  response = HttpResponse(content_type='image/jpeg')
  response['Cache-Control'] = 'max-age=3600000'
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
  photos_count = Photo.all().filter('tag%s =' % tag_id, True).count()
  photos = [p.key().name() for p in Photo.all().filter('tag%s =' % tag_id, True).order('time').fetch(NUMBER_OF_PHOTOS, start)]
  table = []
  bigimage_urls = []
  for cnt, pic_id in enumerate(photos):
    bigimage_urls.append((cnt + 49,
                          "/tag/%s/%s/%s" % (tag_id, page_id, pic_id)))
    if cnt % NUMBER_OF_COLUMNS == 0:
      row = []
      table.append(row)
    row.append(pic_id)
  page_list = get_pages(tag, page_id)
  no_of_pages = ceil_divide(photos_count, NUMBER_OF_PHOTOS)
  next = page_id + 1 if page_id < no_of_pages else None
  previous = page_id -1 if page_id > 1 else None
  return render_to_response('tag.html', 
                            {'pics': table,
                            'bigimage_urls': bigimage_urls,
                            'name': tag.name,
                            'pages': page_list,
                            'tag_id': tag_id,
                            'page_id': page_id,
                            'source': '../' + tag_id,
                            'next': next,
                            'previous': previous,
                            'color': tag.color,})

def tag_loading_page(request, tag_id):
  tag = Tag.get_by_key_name(str(tag_id))
  return render_to_response('tag_loading.html', 
                            {'name': tag.name,
                            'count': tag.count,
                            'tag_id': tag_id,
                            'color': tag.color})
 
def get_pages(tag, page_id):
  no_of_photos = len(tag.photo_list)
  no_of_pages = ceil_divide(no_of_photos, NUMBER_OF_PHOTOS)
  page_list = []
  for page in range(1, no_of_pages):
    start = page * NUMBER_OF_PHOTOS + 1
    end = start + NUMBER_OF_PHOTOS - 1
    """ Normal case """
    page_list.append((page, "%s - %s" % (start, end), 
                      "/tag/%s/%s" % (tag.key().name(), page)))
  """ Last case """
  start = (no_of_pages - 1) * NUMBER_OF_PHOTOS + 1
  end = no_of_photos
  page_list.append((no_of_pages, "%s - %s" % (start, end),
                    "/tag/%s/%s" % (tag.key().name(), no_of_pages)))
  return page_list

def photo_page(request, tag_id, page_id, photo_id):
  tag = Tag.get_by_key_name(tag_id)
  source = "/tag/%s/%s" % (tag_id, page_id)
  photo = Photo.get_by_key_name(photo_id)
  previous, next = photo.neighbours(tag)
  return render_to_response('photo.html',
                      {'image': photo_id,
                       'name': tag.name,
                       'source': source,
                       'previous': previous,
                       'next': next,
                       'color': tag.color})
  
