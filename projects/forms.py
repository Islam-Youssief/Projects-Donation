from django.forms import ModelForm
from django import forms
from django.db import models
from .models import Project , ProjectPictures , Donation


class AddCommentForm(forms.Form):
    comment = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Your Comment Here...'}), max_length=100, required = True)

class DateInput(forms.DateInput):
    input_type = 'date'

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['project_name', 'owner', 'category',
                  'details', 'tags', 'target', 'start_date', 'end_date']
        widgets = {
            'start_date': DateInput(),
            'end_date': DateInput(),
            'owner': forms.HiddenInput() 
        }


class PictureForm(ModelForm):
    # pic = forms.ImageField(label='Upload Images')
    class Meta:
        model = ProjectPictures
        fields = ['picture']

class AddRate(forms.Form):
    MY_CHOICES = [('1','one'), ('2','two')]
    rating = forms.ChoiceField(widget=forms.RadioSelect, choices=MY_CHOICES)

class DonationForm(ModelForm):
    class Meta:
        model = Donation
        fields = ['amount', 'user' , 'project' ]
        widgets = {'project': forms.HiddenInput() , 'user': forms.HiddenInput()}
