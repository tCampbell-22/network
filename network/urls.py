
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('register/', views.register, name="register"),
    path('create/', views.create, name="create"),
    path('like/', views.like),
    path('follow/', views.follow),
    path('following/', views.following, name="following"),
    path('edit/', views.edit),
    path('profile/<str:name>', views.profile_view, name="profile"),
    #path("<str:username>/profile", views.profile_view, name="profile"),
]
