from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField
from .models import Profile
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.forms import SelectDateWidget
# from django.forms.extras.widgets Django < 1.9
from django.utils import timezone


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    password1=forms.CharField(widget=forms.PasswordInput)
    password2=forms.CharField(widget=forms.PasswordInput)
   
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserFormlog(forms.Form):
    username= forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    captcha = CaptchaField()

class AddResourceForm(forms.Form):
    subject_name= forms.CharField()
    subcategory = forms.CharField()
    details = forms.CharField()
    url = forms.URLField(label='Your website', required=False)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('full_name','about_yourself','Education','Experience','skills','profile_photo','Work','resume','interest1')
        
