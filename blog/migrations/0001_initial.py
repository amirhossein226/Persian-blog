# Generated by Django 5.1.1 on 2024-09-30 09:57

import blog.mytools
import django.db.models.deletion
import django.utils.timezone
import taggit.managers
import tinymce.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='عنوان')),
                ('slug', models.SlugField(allow_unicode=True, blank=True, max_length=255, unique_for_date='publish')),
                ('description', models.TextField(verbose_name='توضیح مختصر')),
                ('body', tinymce.models.HTMLField(verbose_name='متن کامل')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('publish', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('PB', 'منتشر شده'), ('DF', 'در انتظار تایید')], default='DF', max_length=2)),
                ('photo', models.ImageField(blank=True, null=True, upload_to=blog.mytools.create_image_path)),
                ('likes_count', models.PositiveIntegerField(default=0)),
                ('authors', models.ManyToManyField(related_name='posts', to=settings.AUTH_USER_MODEL)),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='تگ ها')),
                ('users_like', models.ManyToManyField(blank=True, related_name='posts_liked', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-publish'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='متن')),
                ('author', models.CharField(max_length=40, verbose_name='نام')),
                ('email', models.EmailField(max_length=254, verbose_name='آدرس ایمیل')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='blog.post')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['-publish'], name='blog_post_publish_bb7600_idx'),
        ),
        migrations.AddIndex(
            model_name='comment',
            index=models.Index(fields=['-created'], name='blog_commen_created_79f39f_idx'),
        ),
    ]
