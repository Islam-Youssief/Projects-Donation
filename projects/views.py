from django.shortcuts import redirect, render
from django.http import HttpResponse
import datetime
import math
from django.db.models import Avg, Count, Q, Sum
from .models import Project, ProjectRate, Comment, ProjectPictures, Category, ReportedProject, Comment, ReportedComment, Donation
from django.forms import modelformset_factory
from .forms import AddCommentForm, AddRate
from projects.forms import ProjectForm, PictureForm, DonationForm
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
            return redirect("index")
            # return HttpResponse("project added and redirect to user profile")
    else:
        picture_form = ImageFormSet(queryset=ProjectPictures.objects.none())
        project_form = ProjectForm(initial={"owner":request.session['_auth_user_id']})
        return render(request, 'projects/create_project.html/', {'project_form': project_form, 'picture_form': picture_form})


# fatema

def project_details(request, id):
    project = Project.objects.get(id=id)
    rates = list(project.projectrate_set.values())
    avgRate = ProjectRate.objects.filter(project_id=id).aggregate(Avg('rate'))
    if avgRate['rate__avg'] == None:
        avgRate['rate__avg'] = "0"
    projectimage = project.projectpictures_set.first()
    if projectimage != None:
        projectimage = projectimage.picture.url
        picturesObjects = project.projectpictures_set.all()
        pictures = []
        for picture in picturesObjects:
            pictures.append(picture.picture.url)

    # Adding Comments
    if request.method == 'GET':
        commentForm = AddCommentForm()
        add_rate = AddRate()
    else:
        commentForm = AddCommentForm(request.POST)
        print(commentForm.is_valid())
        if commentForm.is_valid():
            comment = Comment()
            print(request.POST)
            comment.comment = request.POST['comment']
            comment.user_id = 1  # Logged in user
            comment.project_id = id
            comment.save()
    # Checking on Donations
    target = project.target * 0.25
    amount = 0
    donations = Donation.objects.filter(project_id=id)
    for donation in donations:
        amount = amount + donation.amount

    # Getting All Comments
    comments = Comment.objects.filter(project_id=id)

    context = {
        "project": project,
        "avgRate": range(int(avgRate['rate__avg'])),
        "stars": range((5 - int(avgRate['rate__avg']))),
        "rates": rates,
        "pictures": pictures,
        "comment": commentForm,
        "target": target,
        "amount": amount,
        "comments": comments,
        "rate": add_rate
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


def projectDonate(request, id):
    project = Project.objects.get(id=id)
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            result = Donation.objects.filter(
                Q(project_id=id) & Q(user_id=request.POST['user'])).count()
            print(result)
            if(result > 0):
                print("hjhjhj")
                obj = Donation.objects.filter(Q(project_id=id) & Q(
                    user_id=request.POST['user'])).first()
                amount_value = getattr(obj, 'amount')
                Donation.objects.filter(Q(project_id=id) & Q(user_id=request.POST['user'])).update(
                    amount=amount_value + int(request.POST['amount']))
            else:
                donate_form = form.save(commit=False)
                donate_form.save()

            print(result)
            return redirect("index")
            # return HttpResponse("donations has been added and redirect to user profile")
    else:
        donate_form = DonationForm(initial={"project": id , "user":request.session['_auth_user_id']})
        return render(request, 'projects/donate_project.html/', {'donate_form': donate_form, "project":  project})


def search(request):
    query = request.GET.get('q')
    result = []
    # get the query result
    if query:
        result = Project.objects.filter(
            Q(project_name__icontains=query) |
            Q(project_name__icontains=query)
        )
    resultList = []

    for project in result:
        print(project)
        resultList.append({
            'id': project.id,
            'project_name': project.project_name,
            'details': project.details,
            'start_date': project.start_date,
        })
    return render(request, 'search.html', {'results': resultList})

    Project.objects.filter(Q(project_name__icontains="project") | Q(
        details__icontains="project"))


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
# return render(request, 'projects/project_page.html', {'comment':
# commentForm})
def report_project(request, id):
    user_id = request.session['_auth_user_id']
    reported_projects = ReportedProject.objects.filter(project_id=id)
    user_reports = reported_projects.filter(user_id=user_id)
    if user_reports.count() > 0:
        return redirect('project_details', id)
    else:
        project = ReportedProject()
        project.project_id = id
        project.user_id = user_id
        project.is_reported = 0
        project.save()
        final_projects = ReportedProject.objects.filter(project_id=id)
        if final_projects.count() >= 5:
            report_project = Project.objects.get(id=id)
            report_project.is_reported = 1
            report_project.save()
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
    user_id = request.session['_auth_user_id']
    reported_comments = ReportedComment.objects.filter(comment_id=comment_id)
    user_reports = reported_comments.filter(user_id=user_id)
    if user_reports.count() > 0:
        return redirect('project_details', id)
    else:
        comment = ReportedComment()
        comment.comment_id = comment_id
        comment.user_id = user_id
        comment.is_reported = 0
        comment.save()
        final_comments = ReportedComment.objects.filter(comment_id=comment_id)
        if final_comments.count() >= 5:
            report_comment = Comment.objects.get(id=comment_id)
            report_comment.is_reported = 1
            report_comment.save()
        return redirect('project_details', id)


def viewCategories(request, cid):
    # ISLAM
    projects = get_object_or_404(Category, id=cid)
    categories = Category.objects.all()
    context = {
        "projects": projects.projects,
        "categories": categories,
        "categieNmae": projects.name
    }

    return render(request, "projects/projectHome.html", context)
