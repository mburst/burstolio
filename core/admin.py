from django.contrib import admin

from core.models import *

class CommonMedia:
    js = (
        '//ajax.googleapis.com/ajax/libs/dojo/1.7.2/dojo/dojo.js',
        '/static/core/js/editor.js',
    )
    css = {
        'all': ('/static/core/css/editor.css',),
    }

#Not working on heroku. Will fix later if needed
#admin.site.register(Entry, Media=CommonMedia,)
admin.site.register(Entry)
admin.site.register(Tag)
admin.site.register(Subscriber)