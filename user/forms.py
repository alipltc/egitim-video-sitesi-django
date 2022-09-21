from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.forms import TextInput, EmailInput, Select, FileInput

from home.models import UserProfile


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        widgets = {
            'username'  : TextInput(attrs={'id': 'username'}),
            'email'     : EmailInput(attrs={'id': 'email'}),
            'first_name': TextInput(attrs={'id': 'first_name'}),
            'last_name' : TextInput(attrs={'id': 'last_name'}),
        }

CITY = [
    ('İstanbul', 'İstanbul'),
    ('Ankara', 'Ankara'),
    ('İzmir', 'İzmir'),
]

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone', 'address', 'city', 'country', 'image')
        widgets = {
            'phone': TextInput(attrs={'id': 'phone'}),
            'address': TextInput(attrs={'id': 'address'}),
            'city': Select(attrs={'id': 'city'}, choices=CITY),
            'country': TextInput(attrs={'id': 'country'}),
            'image': FileInput(attrs={'id': 'image'}),
        }