from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required
from account.forms import UserEditForm, ProfileEditForm, UserRegistrationForm
from django.views.decorators.http import require_POST
from django.contrib import messages
from blog.models import Post
from blog.mytools import log_sql
from account.models import Profile
from django.conf import settings
from utils.redis_client import redis_client as r
from django.http import HttpResponse
# Create your views here.


@permission_required(("add_post", "change_post", "delete_post"))
@log_sql
def admin_dashboard(request, section):

    valid_sections = ['published-by-staff']

    if section in valid_sections:
        context = {
            'section': section
        }

        if section == 'published-by-staff':
            posts = Post.objects.filter(
                authors__in=[request.user]).prefetch_related('tags')

            published_ids = [int(id) for id in r.smembers('published:posts')]

            # get the views of posts and convert them to int
            with r.pipeline() as pipe:
                keys = [f"post:{post.id}:view" for post in posts]
                pipe.mget(keys)

                views = [
                    int(view) if view else 0 for view in pipe.execute()[0]
                ]

            # coupling each post with its views
            posts_with_views = list(zip(posts, views))

            published = [
                item for item in posts_with_views if item[0].id in published_ids
            ]
            draft = [
                item for item in posts_with_views if item[0].id not in published_ids
            ]

            context['published'] = published
            context['draft'] = draft

        elif section == "comments":
            return HttpResponse('I am working on this section!')

        # elif secion == ''
        return render(
            request,
            'account/admin_dashboard.html',
            context
        )


def signup(request):
    context = {}
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():

            user = form.save(commit=False)
            password = form.cleaned_data['password1']
            user.set_password(password)
            user.save()

            Profile.objects.create(user=user)
            messages.success(
                request, "از توجه شما سپاس گذاریم.حساب کاربری شما با موفقیت ایجاد شد.هم اکنون می توانید وارد وبسایت شوید.")
            return redirect(reverse('login'))
    else:
        form = UserRegistrationForm()

    context['form'] = form

    return render(
        request,
        'registration/signup.html',
        context
    )


@login_required
@log_sql
def dashboard(request, section):
    context = {
        'section': section
    }

    if section == 'edit':
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        context['user_form'] = user_form
        context['profile_form'] = profile_form

    return render(
        request,
        'account/dashboard.html',
        context
    )


@require_POST
@login_required
def apply_user_edit(request):
    user_form = UserEditForm(
        instance=request.user,
        data=request.POST
    )
    profile_form = ProfileEditForm(
        instance=request.user.profile,
        data=request.POST,
        files=request.FILES
    )
    if user_form.is_valid() and profile_form.is_valid():
        user_form.save()
        profile = profile_form.save()

        messages.success(request, 'تغییرات شما با موفقیت ثبت گردید.')
        return redirect(reverse("account:dashboard", kwargs={'section': 'info'}))
    context = {

        'user_form': user_form,
        'profile_form': profile_form,
        'section': 'edit',
    }
    messages.error(request, "مشکلی رخ داده.")

    return render(
        request,
        'account/dashboard.html',
        context
    )
