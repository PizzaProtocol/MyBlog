from django.contrib.sitemaps import Sitemap

from blog.models import Post


class PostSitemap(Sitemap):
    changeover = 'weekly'
    priority = 0.9

    def items(self):
        return Post.objects.all()

    def lastmod(self, obj):
        return obj. updated_at