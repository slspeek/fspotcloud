import logging

class tracer:
  def __init__(self, func):
    self.calls = 0
    self.func = func
  def __call__(self, request, *args, **kwargs):
    self.calls += 1
    logging.debug("Call %s to %s" % (self.calls, self.func.__name__))
    return self.func(request, *args, **kwargs)
