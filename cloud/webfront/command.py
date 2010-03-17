from appengine_django.models import BaseModel
from google.appengine.ext import db
from datetime import datetime
import logging


# Create your models here.
class Command(BaseModel):
  cmd = db.StringProperty('Command', required=True)
  args = db.ListProperty(str, required=True)
  ctime = db.DateTimeProperty('Creation time', required=True)

def schedule(cmd, args):
  c = Command(cmd=cmd, 
              ctime=datetime.now(),
              args=args)
  c.put()

def get_command():
  oldest_cmd = Command.all().order('ctime').get()
  if oldest_cmd:
    cmd, args  = oldest_cmd.cmd, oldest_cmd.args
    logging.info('Giving cmd: %s args: %s to peerbot' % (cmd, args))
    oldest_cmd.delete()
    return [cmd, args]
  return []
  
def ping():
  return True
