from django.contrib import admin
from .models import CustomUser, Profile
from django.contrib.auth.models import Permission
# Register your models here.


admin.site.register(CustomUser)
admin.site.register(Profile)
admin.site.register(Permission)
