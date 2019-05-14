from django.shortcuts import redirect, render
from django.http import HttpResponse
import datetime
import math
from django.db.models import Avg, Count, Q, Sum
from projects.forms import ProjectForm , PictureForm
from django.forms import modelformset_factory
from .models import Project,ProjectRate,Comment,ProjectPictures, Category, ReportedProject, Comment
from .forms import AddCommentForm



# nourhan
def createProject(request):
    
    ImageFormSet = modelformset_factory(ProjectPictures, form=PictureForm, extra=3) 
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES, queryset=ProjectPictures.objects.none())
        if form.is_valid() and formset.is_valid: 
            project_form = form.save(commit=False)
            project_form.save()
            # field = project_form.cleaned_data['tags']
            # tags =  request.POST['tags'].split(',')
            form.save_m2m()

            for pictureForm in formset.cleaned_data:
                if pictureForm:
                    image = pictureForm['picture']
                    photo = ProjectPictures(project=project_form, picture=image)
                    photo.save()

            ### user profile page
            return HttpResponse("project added and redirect to user profile");
    else:
        picture_form = ImageFormSet(queryset=ProjectPictures.objects.none()) 
        project_form = ProjectForm();
        return render(request, 'projects/create_project.html/',{'project_form': project_form ,'picture_form':picture_form})




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
