# Copyright 2008 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.conf.urls.defaults import *
from webfront.peerreciever import recieve_image, recieve_tag, handle_photo_for_tag, recieve_photo_count, recieve_photo_data
from webfront.command import get_command
from webfront.rpcserver import XMLRPC

rpcserver = XMLRPC()
for func in [recieve_image, recieve_tag, get_command, handle_photo_for_tag, recieve_photo_count, recieve_photo_data]:
  rpcserver.register(func)

urlpatterns = patterns('',
  (r'^cloud/$', 'webfront.views.index'),
  (r'^import/$', 'webfront.models.import_tags'),
  (r'^task/schedule_photo_data_requests/(?P<start>\d+)/(?P<count>\d+)$', 'webfront.peerreciever.schedule_photo_data_requests'),
  (r'^task/schedule_image_requests_for_tag/(?P<tag_id>\d+)/(?P<type>\d+)/(?P<start>\d+)/(?P<count>\d+)$', 'webfront.peerreciever.schedule_image_requests_for_tag'),
  (r'^import/(?P<tag_id>\d+)$', 'webfront.models.import_tag_data'),
  (r'^import_tag/(?P<tag_id>\d+)/(?P<offset>\d+)/(?P<limit>\d+)$', 'webfront.models.import_tag_data_part'),
  (r'^tag/(?P<tag_id>\d+)/(?P<page_id>\d+)$', 'webfront.views.tag_page'),
  (r'^tag_load/(?P<tag_id>\d+)$', 'webfront.views.tag_loading_page'),
  (r'^tag_role/(?P<tag_id>\d+)/(?P<public>\d+)$', 'webfront.models.set_public'),
  (r'^tag/(?P<tag_id>\d+)/(?P<page_id>\d+)/(?P<photo_id>\d+)$', 'webfront.views.photo_page'),
  (r'^tag/$', 'webfront.views.tag_index'),
  (r'^clear_all_tags$', 'webfront.models.clear_all_tags'),
  (r'^clear_all_photo$', 'webfront.models.clear_all_photo'),
  (r'^clear_photo/(?P<photo_id>\d+)$', 'webfront.models.clear_photo'),
  (r'^clear_photo_meta/(?P<photo_id>\d+)$', 'webfront.models.clear_photo_meta'),
  (r'^image/(?P<pic_id>\w+)/(?P<type>\d)$', 'webfront.views.get_image'),
  (r'^cloud/(?P<photo_id>\d+)$', 'webfront.views.detail'),
  (r'^retrieve/(?P<photo_id>\d+)/(?P<type>\d)$', 'webfront.tasks.retrieve'),
  (r'^ping/$','webfront.views.ping_page'),
  (r'^ping_cron/$','webfront.tasks.ping_cron'),
  (r'^cron/schedule_update/$','webfront.tasks.schedule_update'),
  (r'^ajax/progress/$', 'webfront.models.ajax_get_tag_progress'),
  (r'^ajax/photo_at/$', 'webfront.models.ajax_photo_at'),
  url(r'^xmlrpc/$', rpcserver.view, name="xmlrpc"),
)
