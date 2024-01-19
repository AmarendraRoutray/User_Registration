from django import forms
from .models import *

class Userform(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','password','email']
        widgets={'password':forms.PasswordInput}
        help_texts={'username':''}   # for display hints
        
        
class ProfileForm(forms.ModelForm):
    # address=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter address'}))
    class Meta:
        model = Profile
        fields = ['address','profile_pic']
        