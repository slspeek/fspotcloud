#!/usr/bin/env python
 
import xmlrpclib

s = xmlrpclib.ServerProxy('http://localhost:8000')

print s.get_first_id()
