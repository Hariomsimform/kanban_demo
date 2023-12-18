# In your app's forms.py file
from django import forms
from .models import UserDetail, UserProject

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserDetail
        fields = ['user_role', 'user_technology']
        widgets = {
            'user_role': forms.Select(attrs={'class': 'form-control'}),
            'user_technology': forms.Select(attrs={'class': 'form-control'}),
        }


class UserProjectForm(forms.ModelForm):
    class Meta:
        model = UserProject
        fields = ['user', 'project']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'project': forms.Select(attrs={'class': 'form-control'}),
        }
