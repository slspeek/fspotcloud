#!/usr/bin/env python
import xmlrpclib
import time
import logging
import botworker

s = xmlrpclib.ServerProxy('http://localhost:8000/xmlrpc/')

def dispath(cmd, args):
  if cmd == 'push_tag':
    botworker.push_tag(*args)
  elif cmd == 'push_tags':
    botworker.push_tags()
  else:
    print "Do not know how to dispatch %s " % cmd

def main():
  while(True):
    cmdlist = s.get_command()
    if cmdlist:
      #cmd = cmdlist[0]
      cmd, args = cmdlist
      msg = 'Action recieved: %s %s' % (cmd, args)
      dispath(cmd,args)
    else:
      msg = "No action at this time"
    #logging.info(msg)
    print msg
    time.sleep(10)

if __name__ == '__main__':
  main()
