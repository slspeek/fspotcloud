from django.http import HttpResponse
from django.shortcuts import render_to_response
from webfront.models import PhotosStore, PhotosMeta, Tags
from xmlrpc import get_my_server_proxy
import logging
from datetime import datetime
from google.appengine.ext import db
from StringIO import StringIO

def index(request):
  photo_list = PhotosStore.all().order('id')
  return render_to_response('index.html', {'photo_list': photo_list})

def detail(request, photo_id):
  photo = None
  logging.info("We got called with: %s" % photo_id)
  peerserver = get_my_server_proxy()
  photo_id, time, jpeg  = peerserver.get_photo_object(int(photo_id), (500,400))
  key = save(photo_id, time, jpeg)
  return HttpResponse("Server Proxy Loaded.\nYou're looking at photo %s.\nTime: %s" % (photo_id, time))
 
def get_image(request, pic_key):
  response = HttpResponse(content_type='image/jpeg')
  image = db.get(pic_key)
  response.write(image.jpeg)
  logging.info("Served image %s" % image.id)
  return response


def save(photo_id, time, jpeg):
  photo = PhotosStore()
  photo.id = photo_id
  photo.time = datetime.fromtimestamp(time)
  photo.jpeg = db.Blob(jpeg.data)
  photo_key = photo.put()
  logging.info("Stored photo %s with key %s" % (photo_id, photo_key))
  return photo_key
