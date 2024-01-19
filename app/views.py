from django.shortcuts import render

# Create your views here.
from .forms import *

def registration(request):
    UFO=Userform()
    PFO=ProfileForm()
    
    d={'UFO':UFO,'PFO':PFO}
    
    return render(request,'registration.html',d)