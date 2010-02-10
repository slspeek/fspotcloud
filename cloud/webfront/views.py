from django.http import HttpResponse
from django.shortcuts import render_to_response
from webfront.models import Photo
from xmlrpc import get_server_proxy
import logging

def index(request):
  photo_list = Photo.objects.all()
  if photo_list == []:
    photo_list = None
  return render_to_response('index.html', {'photo_list': photo_list})

def detail(request, photo_id):
  photo = None
  logging.info("We got called with: %s" % photo_id)
  peerserver = get_server_proxy('http://speek.xs4all.nl')
  photo_id, time, jpeg  = peerserver.get_photo_object(int(photo_id), (500,400))
  return HttpResponse("Server Proxy Loaded.\nYou're looking at photo %s.\nTime: %s" % (photo_id, time))
 

