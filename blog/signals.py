from blog.models import Post
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
import redis
from django.conf import settings
from utils.redis_client import redis_client as r


@receiver(post_save, sender=Post)
def increase_total_post_count(sender, instance, created, **kwargs):
    if created:
        print("======================================================")
        r.incr('post_counts')
        if instance.status == Post.Status.PUBLISHED:
            r.sadd('published:posts', instance.id)
        else:
            r.sadd('draft:posts', instance.id)

    else:
        pub_post_ids = [int(id) for id in r.smembers("published:posts")]
        drf_post_ids = [int(id) for id in r.smembers('draft:posts')]

        if instance.status == Post.Status.PUBLISHED and instance.id not in pub_post_ids:
            r.sadd('published:posts', instance.id)
            r.srem('draft:posts', instance.id)
        elif instance.status == Post.Status.DRAFT and instance.id not in drf_post_ids:
            r.sadd('draft:posts', instance.id)
            r.srem('published:posts', instance.id)


@receiver(pre_delete, sender=Post)
def update_post_delete(sender, instance, **kwargs):
    if instance.status == Post.Status.PUBLISHED:
        r.srem('published:posts', instance.id)
    else:
        r.srem('draft:posts', instance.id)

    r.incrby('post_counts', -1)
