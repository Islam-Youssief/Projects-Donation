from django.shortcuts import redirect, render
from django.http import HttpResponse
import datetime
import math
from django.db.models import Avg, Count, Q, Sum
from . models import Project,ProjectRate,Comment,ProjectPictures
from django.shortcuts import redirect, render

# Create your views here.


def project_details(requset,id):
    project=Project.objects.get(id=id)
    avg_rate = ProjectRate.objects.filter(project_id=id).aggregate(Avg('rate'))
    if avg_rate['rate__avg'] == None:
        avg_rate['rate__avg'] = "0"
    comments = list(project.comment_set.values())
    # mylist = []
    # for i in project:
    #     if project.tags.all in project.tags.all(): 
    #         mylist.append(project)
    context= {
        "project": project,
        "avg_rate": range(int(avg_rate['rate__avg'])),
        "stars": range((5-int(avg_rate['rate__avg']))),
        "comments":comments
    }
    return render(requset, 'projects/project_page.html/', context)