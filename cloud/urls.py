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

urlpatterns = patterns('',
  (r'^cloud/$', 'webfront.views.index'),
  (r'^import/$', 'webfront.models.import_tags'),
  (r'^import/(?P<tag_id>\d+)$', 'webfront.models.import_tag_data'),
  (r'^import_tag/(?P<tag_id>\d+)/(?P<offset>\d+)/(?P<limit>\d+)$', 'webfront.models.import_tag_data_part'),
  (r'^tag/(?P<tag_id>\d+)/(?P<page_id>\d+)$', 'webfront.views.tag_page'),
  (r'^tag/$', 'webfront.views.tag_index'),
  (r'^clear_meta$', 'webfront.models.clear_meta_data'),
  (r'^clear_store$', 'webfront.models.clear_photo_store'),
  (r'^clear_photo/(?P<photo_id>\d+)$', 'webfront.models.clear_photo'),
  (r'^clear_photo_meta/(?P<photo_id>\d+)$', 'webfront.models.clear_photo_meta'),
  (r'^image/(?P<pic_id>\w+)/(?P<type>\d)$', 'webfront.views.get_image'),
  (r'^cloud/(?P<photo_id>\d+)$', 'webfront.views.detail'),
  (r'^retrieve/(?P<photo_id>\d+)/(?P<type>\d)$', 'webfront.tasks.retrieve'),
  (r'^ping/$','webfront.views.ping_page'),
  (r'^ping_cron/$','webfront.tasks.ping_cron'),
)
