from django.urls import re_path as url
from django.conf.urls import include
from django.conf.urls.static import static
from django.conf import settings

from portal.views import *

urlpatterns = [
    # url(r'', portal, name='portal'),

    # Authentication
    url(r'^login/$', portal_login_view, name='login'),
    url(r'^logout/$', portal_logout_view, name='logout'),

    # Edit mode
    url(r'^edit/$', edit_mode, name='edit_mode'),

    # Factory
    url(r'^factory/$', factory, name='factory'),

    # AJAX endpoints
    url(r'^api/settings/update/$', update_settings, name='update_settings'),

    # Factory management
    url('^api/factories/create/$', create_factory, name='create_factory'),
    url('^api/factories/(?P<factory_id>\d+)/update/$', update_factory, name='update_factory'),
    url('^api/factories/(?P<factory_id>\d+)/delete/$', delete_factory, name='delete_factory'),

    # Section management
    url(r'^api/sections/create/$', create_section, name='create_section'),
    url(r'^api/sections/(?P<section_id>\d+)/update/$', update_section, name='update_section'),
    url(r'^api/sections/(?P<section_id>\d+)/delete/$', delete_section, name='delete_section'),

    # Card management
    url(r'^api/cards/create/$', create_card, name='create_card'),
    url(r'^api/cards/(?P<card_id>\d+)/update/$', update_card, name='update_card'),
    url(r'^api/cards/(?P<card_id>\d+)/delete/$', delete_card, name='delete_card'),
    url(r'^api/cards/(?P<card_id>\d+)/track/$', track_click, name='track_click'),

    url(r'^home/', portal_home, name='home'),
]
