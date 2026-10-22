from django import forms
from django.forms import ModelForm
from .models import labreg

from .models import labbill

class regg(forms.ModelForm):
    class Meta():

        model=labreg
        fields="__all__"


class labbills(forms.ModelForm):
    class Meta():

        model=labbill
        fields="__all__"
