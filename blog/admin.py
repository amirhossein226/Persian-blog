from django.contrib import admin
from .models import Post, Comment
from blog.forms import AdminPostEditForm
# Register your models here.


class TabularComment(admin.TabularInline):
    model = Comment
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = AdminPostEditForm
    inlines = [
        TabularComment,
    ]
    list_display = ['title', 'created', 'updated', 'status']
    filter = ["status", "author"]
    search_fields = ['title', 'description']


admin.site.register(Comment)
