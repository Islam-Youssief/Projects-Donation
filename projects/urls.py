from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from .views import project_details

urlpatterns = [
    path('<int:id>',project_details, name="project_details"),
    # path('<int:id>/comment',add_comment, name="new_comment"),
]
