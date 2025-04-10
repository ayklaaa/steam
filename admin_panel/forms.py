# admin_panel/forms.py
from django import forms

from user_profile.models import TegList
from www.models import MStatus


class MStatusForm(forms.ModelForm):
    class Meta:
        model = MStatus
        fields = ['name']  # Мы будем работать только с полем 'name' статуса

class MTeglistForm(forms.ModelForm):
    class Meta:
        model = TegList
        fields = ['name']
