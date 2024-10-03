from django.contrib.syndication.views import Feed
from django.urls import reverse_lazy
from blog.models import Post


class PostFeed(Feed):
    title = 'Asin Laboratory'
    link = reverse_lazy("blog:post_list")
    description = 'آخرین پست های منتشر شده'

    def items(self):
        return Post.published.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_pubdate(self, item):
        return item.publish
