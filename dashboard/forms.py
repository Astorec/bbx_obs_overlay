from django import forms
from .models import Settings
from django.forms import ModelForm

class SettingsForm(ModelForm):
    class Meta:
        model = Settings
        fields = ['api_key', 'username']