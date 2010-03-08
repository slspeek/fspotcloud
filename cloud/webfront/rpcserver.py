from xmlrpclib import loads, dumps, Fault, ResponseError

from django.http import HttpResponse, HttpResponseNotAllowed
from django.utils.functional import wraps
from django.utils.html import strip_spaces_between_tags
import logging


METHOD_NOT_SUPPORTED = Fault(0, "method not supported")

class XMLRPC(object):
    def __init__(self):
        self.handlers = {}

    def register(self, func, exported_name=None):
        if exported_name == None:
          exported_name = func.__name__
        self.handlers[exported_name] = func

    def view(self, request):
        "view function for handling an XML-RPC request"
        logging.debug("Entering view")
        if request.method != "POST":
            return HttpResponseNotAllowed("POST")

        try:
            args, method = loads(request.raw_post_data)
        except ResponseError:
            return HttpResponseNotAllowed("XML-RPC")

        if method is None:
            return HttpResponseNotAllowed("XML-RPC")

        if method not in self.handlers:
            result = METHOD_NOT_SUPPORTED
        else:
            try:
                logging.debug("Just before trying the function")
                result = self.handlers[method](*args)
            except Fault, fault:
                result = fault

        result = isinstance(result, tuple) and result or (result,)
        result = strip_spaces_between_tags(dumps(result, methodresponse=True))

        response = HttpResponse(mimetype="text/xml")
        response.write(result)
        response["Content-Length"] = len(response.content)
        return response
