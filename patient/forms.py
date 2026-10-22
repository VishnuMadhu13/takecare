from django import forms
from django.forms import ModelForm
from .models import pregister
from .models import booking
from .models import medical_report
from .models import requests
from .models import payment
from .models import d_payment



class ins(forms.ModelForm):
    class Meta():

        model=pregister
        fields="__all__"

class booked(forms.ModelForm):
    class Meta():
        model = booking
        fields = "__all__"

class med(forms.ModelForm):
    class Meta():
        model = medical_report
        fields = "__all__"

class req1(forms.ModelForm):
    class Meta():
        model = requests
        fields = "__all__"

class pays(forms.ModelForm):
    class Meta():
        model = d_payment
        fields = "__all__"