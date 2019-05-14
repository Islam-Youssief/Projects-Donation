from django.shortcuts import redirect, render
from django.http import HttpResponse
import datetime
import math
from django.db.models import Avg, Count, Q, Sum
from .models import Project, ProjectRate, Comment, Category
from django.shortcuts import redirect, render


# Create your views here.


def project_details(requset, id):
    project = Project.objects.get(id=id)
    avg_rate = ProjectRate.objects.filter(project_id=id).aggregate(Avg('rate'))
    if avg_rate['rate__avg'] == None:
        avg_rate['rate__avg'] = "0"

    context = {
        "project":  project,
        "avg_rate": avg_rate
    }
    return render(requset, 'projects/project_page.html/', context)

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