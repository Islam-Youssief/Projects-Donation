from django.shortcuts import redirect, render
from django.http import HttpResponse
import datetime
import math
from django.db.models import Avg, Count, Q, Sum
from .models import Project,ProjectRate,Comment,ProjectPictures, Category, ReportedProject, Comment
from django.shortcuts import redirect, render
from .forms import AddCommentForm


# Create your views here.


def project_details(request, id):
    project = Project.objects.get(id=id)
    avg_rate = ProjectRate.objects.filter(project_id=id).aggregate(Avg('rate'))
    if avg_rate['rate__avg'] == None:
        avg_rate['rate__avg'] = "0"
    comments = list(project.comment_set.values())
    # Adding Comments
    if request.method == 'GET':
        commentForm = AddCommentForm()
    else:
        commentForm = AddCommentForm(request.POST)
        print(commentForm.is_valid())
        if commentForm.is_valid():
            comment = Comment()
            print(request.POST)
            comment.comment = request.POST['comment']
            comment.user_id = 2             #Logged in user
            comment.project_id = id
            comment.save()
   
    context= {
        "project":  project,
        "avg_rate":  range(int(avg_rate['rate__avg'])),
        "stars": range((5-int(avg_rate['rate__avg']))),
        "comments":comments,
        "comment": commentForm
    }
    return render(request, 'projects/project_page.html/', context)

# aml


def index(request):
    rated = ProjectRate.objects.raw('''SELECT projects_projectrate.id, projects_project.project_name, projects_projectrate.rate
                                    FROM projects_project JOIN projects_projectrate
                                    WHERE projects_project.id = projects_projectrate.project_id
                                    ORDER BY projects_projectrate.rate
                                    DESC LIMIT 5''')

    latest = Project.objects.all().order_by('start_date')[:5]
    #rated = ProjectRate.objects.filter(project_id=1).select_related()

    cat = Category.objects.all()

    return render(request, 'index.html', {'hightLatestProject': rated,
                                          'latestProject': latest,
                                          'allCategories': cat 
                                          })

def displaydetails(request, id):
    print(id)
    cat2 = Category.objects.all()
    details = {}
    for c in cat2:
        for key in c:
            print(key)
            print(c[key])
            if key == 'id' and c[key] == id:
                details = c
    return render(request, 'details.html', {'c': details})

# def add_comment(request, id):
#     if request.method == 'GET':
#         commentForm = AddCommentForm()
#     else:
#         commentForm = AddCommentForm(request.POST)
#         print(commentForm.is_valid())
#         if commentForm.is_valid():
#             comment = Comment()
#             print(request.POST)
#             comment.comment = request.POST['comment']
#             comment.user_id = 2
#             comment.project_id = id
#             comment.save()
#     return render(request, 'projects/project_page.html', {'comment': commentForm})