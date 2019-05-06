from django.db import models
from django.conf import settings

from taggit.managers import TaggableManager
import uuid
import os


class Category(models.Model):
    category_name = models.CharField(max_length=50)

    def __str__(self):
        return self.category_name


class Project(models.Model):
    project_name = models.CharField(max_length=50)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    details = models.TextField()
    target = models.IntegerField()
    tags = TaggableManager()
    is_featured = models.BooleanField(default=False)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()

    def __str__(self):
        return self.project_name


class Donation(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    amount = models.IntegerField()

    def __str__(self):
        return self.amount


class ProjectRate(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    rate = models.PositiveIntegerField()

    def __str__(self):
        return self.user + ' rated ' + self.project + ' with rate : ' + self.rate


class ProjectPictures(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='photos/')

    def __str__(self):
        return self.project.title + ' has a new picture .'


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    comment = models.TextField()

    def __str__(self):
        return self.user + ' Comment ' + self.project.title + ' with comment : ' + self.comment


class Reply(models.Model):
    reply = models.TextField()
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    def __str__(self):
        return self.reply + ' On Comment ' + self.comment + ' with user : ' + self.user


class ReportedProject(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    is_reported = models.BooleanField()


class ReportedComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    is_reported = models.BooleanField()


class ReportedReply(models.Model):
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    is_reported = models.BooleanField()
