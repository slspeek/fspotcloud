from django.http import HttpResponse
from django.shortcuts import render_to_response
from webfront.models import *
import logging
from google.appengine.ext import db
from xmlrpc import ping
import xmlrpc
from webfront.bigvar import get_value

NUMBER_OF_COLUMNS = 6

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
  image = load_image(int(pic_id))
  response.write(image.jpeg)
  logging.info("Served image %s" % image.id)
  return response

def tag_index(request):
  tag_list = Tags.all().order('name')
  peer_up = get_value('peer_up')
  if peer_up == 'False':
    peer_up = []
  return render_to_response('tag_index.html', { 'tags': tag_list, 'peer_up': peer_up })

  
def tag_page(request, tag_id):
  tag_id = int(tag_id)
  tag = load_tag_by_id(tag_id)
  table = []
  if tag.list_loaded:
    cnt = 0
    for pic_id in tag.photo_list:
      if cnt % NUMBER_OF_COLUMNS == 0:
        row = []
        table.append(row)
      row.append(pic_id)
      cnt += 1
  return render_to_response('tag.html', {'pics': table,  'name': tag.name })
