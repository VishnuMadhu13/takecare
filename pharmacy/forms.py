from django import forms
from django.forms import ModelForm
from .models import phregister
from .models import bill
from .models import stock



class select(forms.ModelForm):
    class Meta():

        model=phregister
        fields="__all__"


class ins(forms.ModelForm):
    class Meta():

        model=bill
        fields="__all__"

class stocks(forms.ModelForm):
    class Meta():

        model=stock
        fields="__all__"
