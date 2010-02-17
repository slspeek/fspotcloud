from xmlrpc import ping
from django.http import HttpResponse
from webfront.bigvar import set_value

def ping_cron(request):
  peer_up = ping()
  set_value('peer_up', str(peer_up))
  return HttpResponse("ping cron")
