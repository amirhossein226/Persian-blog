from django.db.models.signals import m2m_changed
from blog.models import Post
from django.dispatch import receiver


@receiver(m2m_changed, sender=Post.users_like.through)
def increase_total_post_like(sender, instance, **kwargs):
    instance.likes_count = instance.users_like.count()
    instance.save()
