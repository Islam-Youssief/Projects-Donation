from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm


class UserFormEdit(ModelForm):

    class Meta:
        model = User
        fields = ('username', "first_name", "last_name")


class profileFormEdit(ModelForm):

    class Meta:
        model = Account
        fields = ('facebook_profile', 'country', 'birthdate', 'phone', 'image')


class UserFormAdd(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', "first_name", "last_name",
                  "password1", "password2", "email")


class UserFormPassword(ModelForm):

    class Meta:
        model = User
        fields = ('password',)


class userLoginForm(forms.Form):
    username = forms.CharField(max_length=100, required=True)
    password = forms.CharField(max_length=100, required=True)
