"""enterprise_portal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include
from django.urls import re_path as url
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import RedirectView
from rest_framework.routers import DefaultRouter

from base.views import index
from django.conf.urls.static import static
from django.conf import settings
from portal.views import portal_home

router = DefaultRouter()

urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'', include('portal.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon.ico')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    url(r'^$', index, name='index'),
)
