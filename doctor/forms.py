from django import forms
from django.forms import ModelForm
from .models import dregister
from .models import prescription

from .models import vediocall

class insert(forms.ModelForm):
    class Meta():

        model=dregister
        fields="__all__"

class insert1(forms.ModelForm):
    class Meta():
        model = prescription
        fields = "__all__"


class vedios(forms.ModelForm):
    class Meta():
        model = vediocall
        fields = "__all__"