from appengine_django.models import BaseModel
from google.appengine.ext import db
from datetime import datetime
import logging


# Create your models here.
class Command(BaseModel):
  cmd = db.StringProperty('Command', required=True)
  args = db.ListProperty(str, required=True)
  ctime = db.DateTimeProperty('Creation time', required=True)
  # this property was added to check for existing commands
  args_string = db.StringProperty('Argument string')

def schedule(cmd, args):
  args_string = str(args)
  q = Command.all().filter('cmd = ', cmd).filter('args_string = ', args_string)
  duplicates = q.fetch(1)
  #logging.info('schedule - %s' % duplicates)
  if len(duplicates) == 0:
    c = Command(cmd=cmd, 
                ctime=datetime.now(),
                args=args,
                args_string=args_string)
    c.put()
    logging.debug('scheduled: %s %s' % (cmd, args))
  else:
    logging.debug('Not scheduling')

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
