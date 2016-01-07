"""tmp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include, patterns
from django.core.urlresolvers import get_resolver
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings

import django.views.static

import kb.views

from django.shortcuts import redirect
from django.core.urlresolvers import reverse, reverse_lazy

from django.views.generic.base import RedirectView
import kb.urls
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^$', redirect(reverse(kb.views.kb_collection_edit))),
    # url(r'^$', redirect('/hui')),

    url(r'^', include(kb.urls, namespace='kb')),
    url(r'^select2/', include('django_select2.urls')),
    url(r'^tinymce/', include('tinymce.urls')),
]



if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', django.views.static.serve, {'document_root': settings.MEDIA_ROOT}),
    ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)