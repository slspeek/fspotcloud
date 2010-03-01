from google.appengine.ext import webapp                                        
from google.appengine.ext.webapp.util import run_wsgi_app                      
import logging                                                                 
     
from StringIO import StringIO                                                  
import traceback
import xmlrpclib
from xmlrpcserver.xmlrpcserver import XmlRpcServer
                                                                               
class Application:
    def __init__(self):
        pass                    
        
    def getName(self,meta):                                                    
        return 'example'
        
class XMLRpcHandler(webapp.RequestHandler):                                    
    rpcserver = None
                                
    def __init__(self):         
        self.rpcserver = XmlRpcServer()                                        
        app = Application()                                                    
        self.rpcserver.register_class('app',app)                               
                                                                               
    def post(self):
        request = StringIO(self.request.body)
        request.seek(0)                                                        
        response = StringIO()                                                  
        try:
            self.rpcserver.execute(request, response, None)                    
        except Exception, e:                                                   
            logging.error('Error executing: '+str(e))                          
            for line in traceback.format_exc().split('\n'):                    
                logging.error(line)
        finally:
            response.seek(0)  
                                                                               
        rstr = response.read()                                                 
        self.response.headers['Content-type'] = 'text/xml'                     
        self.response.headers['Content-length'] = "%d"%len(rstr)               
        self.response.out.write(rstr)
                                                                               
application = webapp.WSGIApplication(                                          
                                     [('/xmlrpc/', XMLRpcHandler)],
                                     debug=True)                               
def main():
  run_wsgi_app(application)                                                    
        
if __name__ == "__main__":
    main()

