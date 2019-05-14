from django.shortcuts import redirect, render
from django.http import HttpResponse
import datetime
import math
from django.db.models import Avg, Count, Q, Sum
from .models import Project,ProjectRate,Comment ,ProjectPictures
from django.shortcuts import redirect, render
from projects.forms import ProjectForm , PictureForm
from django.forms import modelformset_factory

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




