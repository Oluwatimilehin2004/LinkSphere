from django import forms # type: ignore
from django.contrib.auth.models import User # type: ignore
from .models import Profile

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring focus:border-blue-300'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring focus:border-blue-300'}),
            'username': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring focus:border-blue-300'}),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic', 'country', 'bio', 'gender']
        widgets = {
            'country': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring focus:border-blue-300'}),
            'bio': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring focus:border-blue-300', 'rows': 4}),
            'gender': forms.Select(attrs={'class': 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring focus:border-blue-300'}),
        }

    
class BannerUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['banner']
       