from django.db import models
from django import forms

# Create your models here.

class EntryForm(forms.Form):
    title = forms.CharField(label="Page Title", max_length = 100, required = True)
    content = forms.CharField(widget = forms.Textarea(attrs = {'required': True, 'cols': 2, 'rows': 1}))

