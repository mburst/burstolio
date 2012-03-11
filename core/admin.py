from django.contrib import admin

from core.models import *

class CommonMedia:
    js = (
        'http://ajax.googleapis.com/ajax/libs/dojo/1.7.2/dijit/dijit.js',
        '/static/core/js/editor.js',
    )
    css = {
        'all': ('/static/core/css/editor.css',),
    }

admin.site.register(Entry, Media=CommonMedia,)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Subscriber)