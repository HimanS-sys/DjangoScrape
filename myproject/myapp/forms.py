from django import forms
from myapp.models import Domain

class DomainForm(forms.ModelForm):
    class Meta:
        model = Domain
        fields = ['name']
