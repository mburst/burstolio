from django.conf import settings
from django.conf.urls import include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

urlpatterns = [
    # Examples:
    url(r'^', include('core.urls')),
    #url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'core/login.html'}, name='login'),
    #url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    #url(r'^register/$', 'core.views.register', name='register'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns