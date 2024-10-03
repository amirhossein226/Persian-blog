from django.contrib.sitemaps import Sitemap
from blog.models import Post


class PostSiteMap(Sitemap):
    changefreq = 'weekly'
    priority = '0.9'

    def items(self):
        return Post.published.all()

    def lastmod(self, item):
        return item.updated


class TagSiteMap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        return Tag.objects.all()

    def location(self, item):
        return revers('blog:post_by_tag', args=[item.slug])
