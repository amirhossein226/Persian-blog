from django.urls import path
from . import views


app_name = 'account'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('dashboard/<str:section>/', views.dashboard, name='dashboard'),
    path('dashboard/edit/info/', views.apply_user_edit, name='apply_user_edit'),
    path('dashboard/admin/<str:section>/',
         views.admin_dashboard, name='admin_dashboard')
]
