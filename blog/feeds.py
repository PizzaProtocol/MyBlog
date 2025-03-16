from django.contrib.syndication.views import Feed
from django.urls import reverse_lazy
from .models import Post
from django.utils.feedgenerator import Rss201rev2Feed

class PrettyFeed(Rss201rev2Feed):
    def write_item(self,  heandler):
        heandler.startElement('rss',{
                "type": "text/xml",
                "href":"/static/rss/rss.xml",
            })
        super().write_items(heandler)


class LatestPostFeed(Feed):
    title = "My Blog"
    link = reverse_lazy('blog:post_list')
    description = "Новый пост в моем блоге"

    def items(self):
        return Post.objects.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content

    def item_pubdate(self, item):
        return item.updated_at