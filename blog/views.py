from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post, Comment
from blog.mytools import log_sql, create_image_path
from blog.forms import CommentForm, PostShareForm, PostEditForm

from account.models import Profile
from taggit.models import Tag

from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Prefetch
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponseNotFound
from django.conf import settings
import os
import json
import redis
from urllib.parse import urljoin
from utils.redis_client import redis_client as r
# Create your views here.
UserModel = get_user_model()


@require_POST
def file_url_constructor(request):

    if request.FILES.get('file'):
        try:
            file = request.FILES.get('file')
            post_id = request.POST.get('post_id')

            post = Post.published.get(id=post_id)

            raw_type = file.content_type
            file_type = 'video' if 'video' in raw_type else 'image'

            incomplete_path = create_image_path(
                post, file.name, file_type=file_type)

            # creating the file path using os library and create_image_path function (located on blog.mytools module)
            file_path = os.path.join(
                settings.MEDIA_ROOT, incomplete_path)

            # create directory for related post in order to store images related to it(if does not exists)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # use chunks() method of django UploadFile class and store image part by part on image_path
            with open(file_path, 'wb+') as path:
                for chunk in file.chunks():
                    path.write(chunk)

            # we used MEDIA_ROOT to store the image, but for return the url for this image, we must use MEDIA_URL
            file_url = urljoin(settings.MEDIA_URL, incomplete_path)
            print(file_url)
            return JsonResponse({'success': True, 'url': file_url})

        except Exception as e:
            print(e)
            return JsonResponse({'success': False, 'error': 'there is a problem'})


def home(request):

    return render(
        request,
        'home.html'
    )

# @permission_required


@permission_required('post.change_post', raise_exception=True)
@login_required
def edit(request, id):
    try:
        post = Post.objects.get(id=id)
    except Exception as e:
        return HttpResponseNotFound('There is a problem with retrive')

    form = PostEditForm(instance=post)

    if request.method == 'POST':

        form = PostEditForm(
            instance=post,
            data=request.POST,
            files=request.FILES
        )
        print(form)

        if form.is_valid():
            form.save()
            messages.success(
                request, 'پست مورد مورد نظر با موفقیت تغییر یافت!')
            print('====================================================')
            return redirect(post.get_absolute_url())
        print(form.errors)
    context = {
        'form': form,
        'post': post,
    }

    return render(
        request,
        'blog/edit.html',
        context
    )


@permission_required('post.delete_post', raise_exception=True)
@login_required
def delete(request):
    # this view will used for edit and delete the post
    if request.method == 'POST':
        post_id = request.POST.get('id')
        try:
            post = Post.published.get(id=post_id)
            post.delete()
            return JsonResponse({'status': 'ok', 'message': "پست مورد نظر با موفقیت حذف شد"})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'مشکلی رخ داده:\n{e}'})
    else:
        return JsonResponse({'error': 'Invalid request method'})


@log_sql
def post_list(request, tag_slug=None):

    all_posts = Post.published.prefetch_related(
        'tags', Prefetch(
            'authors',
            queryset=UserModel.objects.only('id', 'username', 'first_name')
        ),
        Prefetch(
            'archived_by',
            queryset=Profile.objects.only('id')
        )
    ).all()

    with_tag = None
    if tag_slug:
        print('tag')
        all_posts = all_posts.filter(tags__slug=tag_slug)
        with_tag = tag_slug

    paginator = Paginator(all_posts, 6, orphans=3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)

    # get the views related to each post from redis and couple the posts and their views together
    redis_view_keys = [f"post:{post.id}:view" for post in posts]
    views = [int(view) if view else 0 for view in r.mget(redis_view_keys)]
    posts_with_views = [{'post': post, 'view': view}
                        for post, view in zip(posts, views)]
    context = {
        "posts": posts_with_views,
        'tag': with_tag,
        'page': posts
    }
    return render(
        request,
        'blog/post_list.html',
        context
    )


@log_sql
def post_details(request, year, month, day, post_slug):
    post = Post.published.defer(
        'created',
        'status',
        'updated',
        'description'
    ).prefetch_related(
        Prefetch(
            'users_like',
            queryset=UserModel.objects.only('id')
        ),
        Prefetch(
            'authors',
            queryset=UserModel.objects.only('username', 'first_name')
        ),
        Prefetch(
            'comments',
            queryset=Comment.objects.defer(
                'updated', 'email', 'is_active').all()
        )
    ).get(
        publish__year=year,
        publish__month=month,
        publish__day=day,
        slug=post_slug,
    )

    # increase the view of the post on redis database:
    views_count = r.incr(f'post:{post.id}:view')

    form = CommentForm()
    context = {
        'post': post,
        'form': form,
        'views_count': views_count
    }
    return render(
        request,
        'blog/post_details.html',
        context
    )


@login_required
def post_comment(request, post_slug):
    post = Post.published.get(slug=post_slug)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request, 'نظر شما با موفقیت ثبت گردید.')
        else:
            message.error(
                request, 'مشکلی پیش آمده.لطفا مجددا نظر خود را ثبت کنید!')
    return redirect(post.get_absolute_url())


@login_required
def post_share(request, post_slug):
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post_slug
    )

    form = PostShareForm()
    if request.method == "POST":
        form = PostShareForm(request.POST)
        if form.is_valid():
            post_url = request.build_absolute_uri(post.get_absolute_url())

            cd = form.cleaned_data
            name = cd.get('name')
            from_email = cd.get('from_email')
            to_email = cd.get('to_email')
            comment = cd.get('extra_explanation', '')

            subject = (
                f"پیام از طرف {name} ({from_email})"
            )
            message = (
                f"{name} پیشنهاد می کند که پست زیر را در وبسایت ما مطالعه کنید\n"
                f"اگر تمایل به خواندن این مطلب دارید،می توانید از لینکی که در زیر برایتان قرار داده شده به صفحه ی مربوط به این پست وارد شوید:\n\n"
                f"{post_url}\n\n"
                f"توضیخات {name}:{comment}"
            )
            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[to_email],
            )
            messages.success(
                request, 'این پست با موفقیت برای فرد مورد نظر شما فرستاده شد.')
            return redirect(post.get_absolute_url())

    context = {
        'form': form,
    }
    return render(
        request,
        'blog/post_share.html',
        context
    )


@login_required
def like_archive(request):
    post_id = request.POST.get('id')
    action = request.POST.get('action')

    try:
        post = Post.published.get(id=post_id)

        if action == "like":
            post.users_like.add(request.user)
        elif action == 'unlike':
            post.users_like.remove(request.user)
        elif action == 'archive':
            request.user.profile.archived_posts.add(post)
        elif action == 'unarchive':
            request.user.profile.archived_posts.remove(post)
        elif action == 'add-to-read':
            request.user.profile.archived_posts.remove(post)
            request.user.profile.read_posts.add(post)
        else:
            request.user.profile.read_posts.remove(post)
        return JsonResponse({'status': 'ok'})
    except Post.DoesNotExist:
        pass
    return JsonResponse({"status": 'error'})


def check_auth(request):
    print(request.user.is_authenticated)
    return JsonResponse({'logged_in': request.user.is_authenticated})
