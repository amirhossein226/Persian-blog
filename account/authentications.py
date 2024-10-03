from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from account.models import Profile
import requests
User = get_user_model()


class EmailBackend:
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


def create_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'google-oauth2':
        profile, created = Profile.objects.get_or_create(user=user)

        if not created:
            if profile.photo:
                return
        image_url = response.get('picture')
        if image_url:
            download = requests.get(image_url)
            if download.status_code == 200:
                image_name = f'{user.username}_profile_photo.jpg'
                profile.photo.save(
                    image_name,
                    ContentFile(download.content),
                    save=True
                )
