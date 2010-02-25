from xmlrpc import ping
from django.http import HttpResponse
from webfront.bigvar import set_value
from webfront.models import retrieve_photo_from_peer, has_image
import logging

def ping_cron(request):
  peer_up = ping()
  set_value('peer_up', str(peer_up))
  return HttpResponse("ping cron")

def retrieve(request, photo_id, type):
  photo_id = int(photo_id)
  if not has_image(photo_id, type):
    retrieve_photo_from_peer(photo_id, type)
    msg = "Photo %s retrieved of type %s" % (photo_id, type)
  else:
    msg = "Photo %s of type %s was already loaded" % (photo_id, type)
  logging.info(msg)
  return HttpResponse(msg)
