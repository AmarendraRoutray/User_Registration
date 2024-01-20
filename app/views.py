from django.shortcuts import render

# Create your views here.
from .forms import *
from django.http import HttpResponse

def registration(request):
    UFO=Userform()
    PFO=ProfileForm()
    d={'UFO':UFO,'PFO':PFO}
    
    if request.method=='POST' and request.FILES:    # request.FILES used for taking images/files submitted by user through frontend
        ufd=Userform(request.POST)
        pfd=ProfileForm(request.POST,request.FILES)    # here ProfileForm taking two arg because there is ImageField in Profile
        
        if ufd.is_valid() and pfd.is_valid():
            MUFDO=ufd.save(commit=False)        # for modification in data
            pw=ufd.cleaned_data['password']     # taking password from object
            MUFDO.set_password(pw)              # encrypting password(modifying) using set_password function
            MUFDO.save()
            
            MPFDO=pfd.save(commit=False)        
            MPFDO.username=MUFDO                # in profile model we have 3 col but in profile form we have 2 inputField, to avoid error i am giving user obj for username col
            MPFDO.save()
            
            return HttpResponse('Registration Successfull')
        else:
            return HttpResponse('Inavlid Data')
    
    
    return render(request,'registration.html',d)