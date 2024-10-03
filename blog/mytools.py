from django.db import connection, reset_queries
import functools
from django.utils.text import slugify
# to create a path for images related to each post


def log_sql(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        reset_queries()
        function = func(*args, **kwargs)
        for query in connection.queries:
            print("-"*20)
            print(f"{query['time']}: {query['sql']}")
        return function
    return wrapper


def create_image_path(instance, filename, **kwargs):
    urls = {
        'image': f"posts/{instance.slug}/images/{instance.created.year}/{instance.created.month}/{instance.created.day}/{filename}",
        'video': f"posts/{instance.slug}/videos/{instance.created.year}/{instance.created.month}/{instance.created.day}/{filename}"
    }
    file_type = kwargs.get('file_type', None)
    return (urls[file_type] if file_type else urls['image'])
