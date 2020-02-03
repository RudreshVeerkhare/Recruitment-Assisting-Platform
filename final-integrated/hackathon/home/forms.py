#create forms over here
from django import forms

class FilterForm(forms.Form):
    tags = forms.CharField(max_length=500, help_text="enter ',' seperated words")

class FileUploadForm(forms.Form):
    name = forms.CharField(max_length=100,min_length=1,help_text="Enter your name")
    resume = forms.FileField(help_text="Enter your resume in .docx format")