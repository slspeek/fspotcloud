#!/usr/bin/env python
import xmlrpclib
import time
import logging
from botworker import push_tags, push_tag, push_photo, push_tag_data
from config import SERVER_URL

s = xmlrpclib.ServerProxy(SERVER_URL)
register = {'push_tags': push_tags,
            'push_tag': push_tag,
            'push_photo': push_photo,
            'push_tag_data': push_tag_data, }

def dispath(cmd, args):
  func = register[cmd]
  if func:
    func(*args)
  else:
    print "Do not know how to dispatch %s " % cmd

def main():
  while(True):
    cmdlist = s.get_command()
    if cmdlist:
      cmd, args = cmdlist
      msg = 'Action recieved: %s %s' % (cmd, args)
      dispath(cmd,args)
    else:
      msg = 'No action at this time'
    logging.info(msg)
    print msg
    time.sleep(10)

if __name__ == '__main__':
  main()
