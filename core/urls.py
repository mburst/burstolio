from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns('core.views',
    url(r'^$', 'blog', name='home'),
    url(r'^blog/$', 'blog', name='blog'),
    url(r'^blog/(?P<slug>.*)/$', 'entry', name='entry'),
    url(r'^subscribe/$', 'subscribe', name='subscribe'),
    url(r'^unsubscribe/$', 'unsubscribe', name='unsubscribe'),
    url(r'^contact/$', 'contact', name='contact'),
    url(r'^alertthepress/$', 'alert_the_press', name='alert-the-press'),
    url(r'^portfolio/', TemplateView.as_view(template_name="core/portfolio.html")),
    url(r'^resume/', TemplateView.as_view(template_name="core/resume.html")),
)

