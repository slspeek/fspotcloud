from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^cloud/$', 'views.index'),
    (r'^cloud/aap', 'views.index'),
)
