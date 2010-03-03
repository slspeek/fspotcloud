from appengine_django.models import BaseModel
from django.shortcuts import render_to_response
from django.http import HttpResponse
from google.appengine.ext import db
from datetime import datetime
import logging

# Create your models here.
class Commands(BaseModel):
  cmd = db.StringProperty('Command', required=True)
  args = db.ListProperty(str, required=True)
  ctime = db.DateTimeProperty('Creation time', required=True)
  ftime = db.DateTimeProperty('Time the command finished')

def schedule(cmd, args):
  c = Commands(cmd=cmd, 
              ctime=datetime.now(),
              args=args)
  c.put()

def get_command():
  logging.info('Entering get_command')
  oldest_cmd = Commands.all().order('ctime').get()
  if oldest_cmd:
    cmd, args  = oldest_cmd.cmd, oldest_cmd.args
    logging.info('Cmd: %s Args: %s' % (cmd, args))
    oldest_cmd.delete()
    return [cmd, args]
  return []
  

