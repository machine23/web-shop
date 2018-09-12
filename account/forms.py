from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import Profile


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = 'first_name', 'last_name', 'email'


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = 'username', 'email'


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email')


class ProfileForm(forms.ModelForm):
    birth_date = forms.DateField(help_text='Format: YYYY-MM-DD', required=False)
    avatar = forms.ImageField(widget=forms.FileInput, required=False)

    class Meta:
        model = Profile
        fields = 'birth_date', 'avatar'
