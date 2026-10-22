from django import forms
from django.forms import ModelForm
from .models import labreg

from .models import labbill
from .models import labtestcat
from .models import labtest
from .models import testreport

class regg(forms.ModelForm):
    class Meta():

        model=labreg
        fields="__all__"


class labbills(forms.ModelForm):
    class Meta():

        model=labbill
        fields="__all__"


class testcategory(forms.ModelForm):
    class Meta():

        model=labtestcat
        fields="__all__"


class labtestadd(forms.ModelForm):
    class Meta():

        model=labtest
        fields="__all__"

class testsreport(forms.ModelForm):
    class Meta():

        model=testreport
        fields="__all__"


