from django import forms


class AddCommentForm(forms.Form):
    comment = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Your Comment Here...'}), max_length=100, required = True)