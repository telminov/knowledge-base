from django.conf.urls import url
from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import RedirectView
from kb.forms import CustomAuthenticationForm
import kb.views

from django.contrib.auth.views import login, logout

urlpatterns = [
    url(r'^$', RedirectView.as_view(url=reverse_lazy('kb:user_manual_list'))),
    url(r'^upload/$', kb.views.upload, name='upload'),

    # url(r'^collection/list/$', kb.views.kb_collection_list, name='collection_list'),
    # url(r'^collection/add/$', kb.views.kb_collection_edit, name='collection_add'),
    # url(r'^collection/(?P<kb_collection_id>\d+)/$', kb.views.kb_collection_edit, name='collection_edit'),

    url(r'^user_manual/list/$', kb.views.user_manual_list, name='user_manual_list'),
    url(r'^user_manual/add/$', kb.views.user_manual_add, name='user_manual_add'),
    url(r'^user_manual/(?P<user_manual_id>\d+)/$', kb.views.user_manual_edit, name='user_manual_edit'),
    url(r'^user_manual/(?P<user_manual_id>\d+)/detele/$', kb.views.user_manual_delete, name='user_manual_delete'),
    url(r'^user_manual/(?P<user_manual_id>\d+)/view/$', kb.views.user_manual_view, name='user_manual_view'),
    url(r'^user_manual/(?P<view_path>.+)/json/$', kb.views.user_manual_json, name='user_manual_json'),

    url(r'^instruction/add/$', kb.views.instruction_add, name='instruction_add'),
    url(r'^instruction/(?P<pk>\d+)/$', kb.views.instruction_edit, name='instruction_edit'),
    url(r'^instruction/(?P<pk>\d+)/delete/$', kb.views.instruction_delete, name='instruction_delete'),
    url(r'^instruction/list/$', kb.views.instruction_list, name='instruction_list'),

    url(r'^kb_name/$', kb.views.kb_name_list_json),

    url(r'^schema/', kb.views.schema, name='schema'),
    url(r'^login/$', login, {'template_name': 'kb/login.html', 'authentication_form': CustomAuthenticationForm}, name='custom_login'),
    url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),
]
