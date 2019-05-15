from django.shortcuts import redirect, render
from django.http import HttpResponse
import datetime
import math
from django.db.models import Avg, Count, Q, Sum
from .models import Project, ProjectRate, Comment, ProjectPictures, Category, ReportedProject, Comment, ReportedComment , Donation
from django.shortcuts import redirect, render
from projects.forms import ProjectForm, PictureForm
from django.forms import modelformset_factory
from .models import Project, ProjectRate, Comment, ProjectPictures, Category, ReportedProject, Comment
from .forms import AddCommentForm

# nourhan
def createProject(request):

    ImageFormSet = modelformset_factory(
        ProjectPictures, form=PictureForm, extra=3)
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES,
                               queryset=ProjectPictures.objects.none())
        if form.is_valid() and formset.is_valid:
            project_form = form.save(commit=False)
            project_form.save()
            # field = project_form.cleaned_data['tags']
            # tags =  request.POST['tags'].split(',')
            form.save_m2m()

            for pictureForm in formset.cleaned_data:
                if pictureForm:
                    image = pictureForm['picture']
                    photo = ProjectPictures(
                        project=project_form, picture=image)
                    photo.save()

            # user profile page
            return HttpResponse("project added and redirect to user profile")
    else:
        picture_form = ImageFormSet(queryset=ProjectPictures.objects.none()) 
        project_form = ProjectForm();
        return render(request, 'projects/create_project.html/',{'project_form': project_form ,'picture_form':picture_form})


#fatema

def project_details(request, id):
    project = Project.objects.get(id=id)
    rates = list(project.projectrate_set.values())
    avgRate = ProjectRate.objects.filter(project_id=id).aggregate(Avg('rate'))
    if avgRate['rate__avg'] == None:
        avgRate['rate__avg']= "0"    
    projectimage = project.projectpictures_set.first()
    if projectimage != None : 
        projectimage = projectimage.picture.url
        picturesObjects = project.projectpictures_set.all()
        pictures = []
        for picture in picturesObjects:
            pictures.append(picture.picture.url)

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
            comment.user_id = 2  # Logged in user
            comment.project_id = id
            comment.save()
    # Checking on Donations
    target = project.target * 0.25
    amount = 0
    donations = Donation.objects.filter(project_id = id)
    for donation in donations:
        amount = amount + donation.amount

    #Getting All Comments
    comments = Comment.objects.filter(project_id=id)
    


    context= {
        "project": project,
        "avgRate": range(int(avgRate['rate__avg'])),
        "stars": range((5-int(avgRate['rate__avg']))),
        "rates":rates,
        "pictures": pictures,
        "comment": commentForm,
        "target": target,
        "amount": amount,
        "comments": comments
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

    featured = Project.objects.raw('''SELECT projects_project.id, projects_project.project_name, projects_project.details
                                        FROM projects_project
                                        WHERE is_featured = 1
                                        ORDER BY is_featured
                                        LIMIT 5''')

    return render(request, 'index.html', {'hightLatestProject': rated,
                                          'latestProject': latest,
                                          'allCategories': cat,
                                          'featuredProjects': featured
                                          })


def displaydetails(request, id):
    # print(id)
    cat2 = Category.objects.all()
    details = {}
    for c in cat2:
        for key in c:
            print(key)
            print(c[key])
            if key == 'id' and c[key] == id:
                details = c
    return render(request, 'details.html', {'c': details})
   

def search(request):
    form = SearchForm(request.GET)
    if form.is_valid():
        mode = form.cleaned_data.get("mode")
        searching = form.cleaned_data.get("search")
        if mode == "1":
            projects = taggit_tag.objects.filter(name=searching)
            if projects:
                projects = projects[0].project_all()
        else:
            projects = Project.objects.filter(project_name=searching)
    categories = Category.objects.all()
    context = {
        "projects": projects,
        "categories": categories,
        "categieNmae": searching
    }
    return render(request, "projects/view.html", context)


######### aml ########

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
def report_project(request, id):
    project = ReportedProject()
    project.project_id = id
    project.user_id = 2
    project.is_reported = 0
    project.save()
    return redirect('project_details', id)

def cancel_project(request, id):
    project = Project.objects.get(id=id)
    project.delete()
    return redirect('project_details', id)

def delete_comment(request, id, comment_id):
    comment = Comment.objects.get(id=comment_id)
    comment.delete()
    return redirect('project_details', id)

def report_comment(request, id, comment_id):
    comment = ReportedComment()
    comment.comment_id = comment_id
    comment.user_id = 2
    comment.is_reported = 0
    comment.save()
    return redirect('project_details', id)
