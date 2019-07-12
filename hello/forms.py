# forms.py
from django import forms
from .models import Laptop


class imageForm(forms.ModelForm):
    # name = forms.CharField(disabled=True)

    class Meta:
        model = Laptop
        fields = ['Laptop_Img']
