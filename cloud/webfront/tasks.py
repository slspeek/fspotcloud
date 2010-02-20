from xmlrpc import ping
from django.http import HttpResponse
from webfront.bigvar import set_value
from webfront.models import retrieve_photo_from_peer

def ping_cron(request):
  peer_up = ping()
  set_value('peer_up', str(peer_up))
  return HttpResponse("ping cron")

def retrieve(request, photo_id):
  retrieve_photo_from_peer(photo_id)
  return HttpResponse("Photo %s retrieved" % photo_id)
