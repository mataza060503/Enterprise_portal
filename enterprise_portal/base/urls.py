from django.urls import re_path as url
from base.views import *

urlpatterns = [
    url(r'', index, name='index'),
]
