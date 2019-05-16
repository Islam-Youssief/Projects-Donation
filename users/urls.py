from django.urls import path, re_path
from .views import *
app_name = "users"
urlpatterns = [
    path("login", loginuser, name="login"),
    path("logout", logout_view, name="logout"),
    path("profile/<int:uid>", profile, name="profile"),
    path("register", signup_new_user, name="register"),
    path("edit/<int:uid>", editprofile, name="edit"),
    path("delete", deleteAccount, name="delete"),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            activate, name='activate')
]
