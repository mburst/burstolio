from django.conf.urls import url
from django.views.generic import TemplateView

from core import views
from core.feeds import rss_feed, atom_feed

app_name = 'core'

urlpatterns = [
    url(r'^$', views.blog, name='home'),
    url(r'^blog/$', views.blog, name='blog'),
    url(r'^blog/(?P<slug>.*)/$', views.entry, name='entry'),
    url(r'^subscribe/$', views.subscribe, name='subscribe'),
    url(r'^unsubscribe/$', views.unsubscribe, name='unsubscribe'),
    url(r'^contact/$', TemplateView.as_view(template_name="core/contact.html")),
    url(r'^alertthepress/$', views.alert_the_press, name='alert-the-press'),
    url(r'^rss/$', rss_feed()),
    url(r'^atom/$', atom_feed()),
]