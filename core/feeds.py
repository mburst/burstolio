from core.models import Entry

from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.utils import text

class rss_feed(Feed):
    title = "Max Burstein's Blog"
    link = "/blog/"
    description = "Latest posts from Max Burstein's technical blog"
    
    def items(self):
        return Entry.objects.filter(published=True)[:5]
    
    def item_description(self, item):
        return text.Truncator(item.content).words(83, None, True)
    
    def item_pubdate(self, item):
        return item.date
    
    
class atom_feed(rss_feed):
    feed_type = Atom1Feed
    subtitle = rss_feed.description