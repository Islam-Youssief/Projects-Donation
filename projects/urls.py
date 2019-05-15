from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from .views import project_details ,createProject, report_project, cancel_project

urlpatterns = [
    path('<int:id>',project_details, name="project_details"),
    path('create',createProject,name="create_project"),
    path('<int:id>/report',report_project,name="report_project"),
    path('<int:id>/cancel',cancel_project,name="cancel_project")
]
