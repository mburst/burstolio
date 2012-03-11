from django.contrib import admin

from core.models import *

class CommonMedia:
    js = (
        '/static/core/js/dojo.js',
        '/static/core/js/editor.js',
    )
    css = {
        'all': ('/static/core/css/editor.css',),
    }

admin.site.register(Entry, Media=CommonMedia,)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Subscriber)