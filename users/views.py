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
from .tokens import account_activation_token


def signup_new_user(request):
    categories = Categories.objects.all()
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
                messages.success(request, "you have sucessfully Registered your account.. "
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
        return redirect("projects:home")


# go Profile
def profile(request, uid):
    user2 = get_object_or_404(User, id=uid)
    categories = Categories.objects.all()
    if request.user.id == user2.id:
        flag = 1
    else:
        flag = 0
    context = {
        "userprofile": user2,
        "userProject": user2.projects_set.all(),
        "categories": categories,
        "flag": flag,
        "pcount": user2.projects_set.count(),
        "suppliers": user2.supplier_set.all(),
        "scount": user2.supplier_set.count()
    }
    return render(request, "users/profile.html", context)


# logout
@login_required()
def logout_view(request):
    logout(request)
    return redirect("/projects/home")


# login
def loginuser(request):
    categories = Categories.objects.all()
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
                    return redirect("projects:home")
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
        return redirect("projects:home")


# testing

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
        return redirect('projects:home')
    else:
        return HttpResponse('<h1> 404 </h1>')
