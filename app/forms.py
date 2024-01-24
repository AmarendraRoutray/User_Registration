from django import forms
from .models import *

class Userform(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','password','email']
        widgets={
            'username':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Username'}),
            'password':forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Password'}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter Email'})
            }
        help_texts={'username':''}   # for display hints
        
        
class ProfileForm(forms.ModelForm):
    # address=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter address','rows':3,'col':3}))
    class Meta:
        model = Profile
        fields = ['address','profile_pic']
        widgets={
            'profile_pic':forms.ClearableFileInput(attrs={'class':'form-control'}),
            'address':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter address'})
        }