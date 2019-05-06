from django.contrib import admin

# Register your models here.
from .models import Category, Project, Donation, ProjectRate, ProjectPictures, Comment, Reply, ReportedProject, ReportedComment, ReportedReply
admin.site.register(Category)
admin.site.register(Project)
admin.site.register(Donation)
admin.site.register(ProjectRate)
admin.site.register(ProjectPictures)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(ReportedProject)
admin.site.register(ReportedComment)
admin.site.register(ReportedReply)
