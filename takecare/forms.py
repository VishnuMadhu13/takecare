from django import forms
from django.forms import ModelForm
from .models import time


class times(forms.ModelForm):
    class Meta():

        model=time
        fields="__all__"