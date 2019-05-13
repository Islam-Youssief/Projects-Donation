from django.shortcuts import redirect, render
from django.http import HttpResponse
import datetime
import math
from django.db.models import Avg, Count, Q, Sum
from .models import Project,ProjectRate,Comment
from django.shortcuts import redirect, render


# Create your views here.


def project_details(requset,id):
    project=Project.objects.get(id=id)
    avg_rate = ProjectRate.objects.filter(project_id=id).aggregate(Avg('rate'))
    if avg_rate['rate__avg'] == None:
        avg_rate['rate__avg'] = "0"

    context= {
        "project":  project,
        "avg_rate": avg_rate
    }
    return render(requset, 'projects/project_page.html/', context)

#aml

def index(request):
    test=ProjectRate.objects.raw('''SELECT projects_projectrate.id, projects_projectrate.rate 
                                    FROM projects_project JOIN projects_projectrate
                                    WHERE projects_project.id = projects_projectrate.project_id
                                    ORDER BY projects_projectrate.rate 
                                    DESC LIMIT 5''')

    data = Project.objects.all().order_by('start_date')[:5]
    #rated = ProjectRate.objects.filter(project_id=1).select_related() 
    return render(request,'index.html',{'latestProject':data,
                                        'hightLatestProject':test
                })
    # to enter new category <a href=" {%url 'my_category'  %}"> category </a>   47 -- 3:11 min