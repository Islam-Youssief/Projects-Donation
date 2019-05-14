from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from .views import project_details ,createProject

urlpatterns = [
    path('<int:id>',project_details, name="project_details"),
    path('create',createProject,name="create_project")
]
