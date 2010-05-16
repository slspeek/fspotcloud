from django.http import HttpResponse
from webfront.bigvar import set_value
from webfront.command import ping, schedule
import logging

def ping_cron(request):
  peer_up = ping()
  set_value('peer_up', str(peer_up))
  logging.info('Ping cron')
  return HttpResponse("ping cron")

def schedule_update(request):
  schedule('send_photo_count', [])
  return HttpResponse("schedule send_photo_count")
