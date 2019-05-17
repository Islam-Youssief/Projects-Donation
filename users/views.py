from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.utils.encoding import force_bytes, force_text
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib import messages
from users.forms import *
from projects.models import *
# from users.forms import UserFormEdit, profileFormEdit, UserFormAdd, UserFormPassword, userLoginForm
from .tokens import account_activation_token


def signup_new_user(request):
    categories = Category.objects.all()
    context = {
        "categories":  categories,
    }
    if not request.user.is_authenticated:
        if request.POST:
            formuser = UserFormAdd(request.POST)
            formprofile = profileFormEdit(request.POST, request.FILES)
            if formuser.is_valid() and formprofile.is_valid():
                formuser.save()
                userreg = User.objects.latest('id')
                userreg.is_active = False
                userreg.save()
                newprof = Account.objects.get(user=userreg)
                newprof.phone = formprofile.cleaned_data.get("phone")
                newprof.image = formprofile.cleaned_data.get("image")
                newprof.save()
                current_site = get_current_site(request)
                mail_subject = 'Projects Donation Site - Activation Email'
                message = render_to_string('users/acc_active_email.html', {
                    'user': userreg,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(userreg.pk)),
                    'token': account_activation_token.make_token(userreg),
                })
                to_email = formuser.cleaned_data.get('email')
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()
                messages.success(request, "sucess Register -- Welcom -- "
                                          "Please confirm your email address to complete the registration  ")
                return HttpResponse('<center><h1>A confirmation Email was sent to your email .. </h1></center>')
            else:
                messages.error(request, formuser.errors)
                messages.error(request, formprofile.errors)
                context["data"] = request.POST
                return render(request, "users/register.html", context)
        else:
            return render(request, "users/register.html", context)
    else:
        # return redirect("projects:home")
        return redirect("projects:index")
        # return render(request, 'index.html')


# go Profile
def profile(request, uid):
    user2 = get_object_or_404(User, id=uid)
    categories = Category.objects.all()
    if request.user.id == user2.id:
        flag = 1
    else:
        flag = 0
    context = {
        "userprofile": user2,
        "userProject": user2.project_set.all(),
        "categories": categories,
        "flag": flag,
        "pcount": user2.project_set.count(),
        # "suppliers": user2.supplier_set.all(),
        # "scount": user2.supplier_set.count()
    }
    return render(request, "users/profile.html", context)


# delete account
@login_required()
def deleteAccount(request):
    user2 = request.user
    form = UserFormPassword(request.POST)
    if form.is_valid():
        print("wwww")
        user = authenticate(username=user2.username,
                            password=form.cleaned_data.get("password"))
        if user is not None:
            user.delete()
            messages.success(request, "Delete Account Sucess")
            # return redirect("/projects/home")
            return redirect("projects:index")
            # return render(request, 'index.html')
        else:
            messages.error(request, "Enter Valid password ")
    messages.error(request, form.errors)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


# logout
@login_required()
def logout_view(request):
    logout(request)
    # return redirect("/projects/home")
    return redirect("projects:index")
    # return render(request, 'index.html')


# login
def loginuser(request):
    categories = Category.objects.all()
    context = {
        "categories": categories,
    }
    if not request.user.is_authenticated:
        if request.POST:
            form = userLoginForm(request.POST)
            if (form.is_valid()):
                users = authenticate(username=form.cleaned_data.get("username"),
                                     password=form.cleaned_data.get("password"))
                if users is not None:
                    login(request, users)
                    messages.success(
                        request, "You have successfully registered your account. ")
                    # return redirect("projects:home")
                    return redirect("projects:index")
                    # return render(request, 'index.html')
                else:
                    context["data"] = request.POST['username']
                    messages.error(
                        request, "password or user name is incoorect")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            # No backend authenticated the credentials
            else:
                messages.error(request, form.errors)
                context["data"] = request.POST
                return render(request, "users/login.html", context)
        else:
            return render(request, "users/login.html", context)
    else:
        # return redirect("projects:home")
        return redirect("projects:index")
        # return render(request, 'index.html')


# edit profile
@login_required()
def editprofile(request, uid):
    user2 = get_object_or_404(User, id=uid)
    categories = Category.objects.all()
    context = {
        "userprofile": user2,
        "categories": categories,
    }
    if request.POST:
        formmuser = UserFormEdit(request.POST, instance=user2)
        formprofile = profileFormEdit(
            request.POST, instance=user2.account, files=request.FILES)
        if formprofile.is_valid() and formmuser.is_valid():
            formmuser.save()
            formprofile.save()
            messages.success(request, "Update information Success")
            return redirect("users:profile", user2.id)
        else:
            messages.error(request, formprofile.errors)
            messages.error(request, formmuser.errors)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return render(request, "users/editprofile.html", context)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(
            request, "You have successfully registered to projects donations..")
        # return redirect('projects:home')
        return redirect('projects:index')
        # return render(request, 'index.html')
    else:
        return HttpResponse('<h1> 404 </h1>')
