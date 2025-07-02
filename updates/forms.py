from django import forms
from .models import VersionUpdate

class VersionUpdateForm(forms.ModelForm):
    class Meta:
        model = VersionUpdate
        fields = ['version', 'summary', 'highlights']
        widgets = {
            'summary': forms.Textarea(attrs={'rows': 4}),
            'highlights': forms.Textarea(attrs={'rows': 2}),
        } 