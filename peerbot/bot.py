#!/usr/bin/env python
import xmlrpclib
import time
import logging
from botworker import push_tags, push_photo
from botworker import push_tag_data, send_photo_count, send_photo_data
from config import SERVER_URL

s = xmlrpclib.ServerProxy(SERVER_URL)
register = {'push_tags': push_tags,
            'push_photo': push_photo,
            'push_tag_data': push_tag_data,
            'send_photo_count': send_photo_count,
            'send_photo_data': send_photo_data,}

def dispath(cmd, args):
  print 'In  dispatch'
  func = register[cmd]
  if bool(func):
    try:
      func(*args)
    except Exception, ( e,) :
      print "Excepted an fault running %s %s %s" % (cmd, args, e)
  else:
    print "Do not know how to dispatch %s " % cmd

def main():
  while(True):
    try:
      cmdlist = s.get_command()
      if cmdlist:
        cmd, args = cmdlist
        print 'Action recieved: %s %s' % (cmd, args)
        no_action = False
        dispath(cmd,args)
      else:
        print 'No action at this time'
        no_action = True
      if no_action:
        print 'Sleeping for 10 seconds'
        time.sleep(10)
    except Exception, e:
      print "Unexpected error: %s, resuming in a short while" % (e)
      time.sleep(1)

if __name__ == '__main__':
  main()
