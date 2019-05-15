from django.forms import ModelForm
from django import forms
from django.db import models
from .models import Project , ProjectPictures , Donation


class DateInput(forms.DateInput):
    input_type = 'date'

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['project_name', 'owner', 'category',
                  'details', 'tags', 'target', 'start_date', 'end_date']
        widgets = {
            'start_date': DateInput(),
            'end_date': DateInput()
        }


class PictureForm(ModelForm):
    # pic = forms.ImageField(label='Upload Images')
    class Meta:
        model = ProjectPictures
        fields = ['picture']


class DonationForm(ModelForm):
    class Meta:
        model = Donation
        fields = ['amount', 'user' , 'project' ]
        widgets = {'project': forms.HiddenInput()}