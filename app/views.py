from django.shortcuts import render

# Create your views here.
from .forms import *
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse

def registration(request):
    UFO=Userform()
    PFO=ProfileForm()
    d={'UFO':UFO,'PFO':PFO}
    
    if request.method=='POST' and request.FILES:    # request.FILES used for taking images/files submitted by user through frontend
        UFDO=Userform(request.POST)
        PFDO=ProfileForm(request.POST,request.FILES)    # here ProfileForm taking two arg because there is ImageField in Profile model/form
        
        if UFDO.is_valid() and PFDO.is_valid():
            MUFDO=UFDO.save(commit=False)        # for modification in data
            pw=UFDO.cleaned_data['password']     # taking password from object
            MUFDO.set_password(pw)              # encrypting password(modifying) using set_password function
            MUFDO.save()
            
            MPFDO=PFDO.save(commit=False)        
            MPFDO.username=MUFDO                # in profile model we have 3 col but in profile form we have 2 inputField, to avoid error i am giving user obj for username col
            MPFDO.save()
            
            send_mail('Registration',
                      'Thank you for registering in MyEra',
                      'amarendraroutray6@gmail.com',
                      [MUFDO.email],
                      fail_silently=True
                      )
            
            messages.success(request,'Registration Successfull')
            return HttpResponseRedirect('/registration')
        else:
            messages.warning(request,'Registration failed')
            return HttpResponseRedirect('/registration')
    
    
    return render(request,'registration.html',d)



def home(request):
    
    if request.session.get('username'):
        username = request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)
    
    return render(request,'home.html')


def user_login(request):
    if request.method == "POST":
        username = request.POST['un']
        password = request.POST['pw']
        
        AUO = authenticate(username=username,password=password)
        
        if AUO and AUO.is_active :
            login(request, AUO)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
    
    return render(request,'user_login.html')



@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


@login_required
def profile_display(request):
    un = request.session.get('username')
    UO = User.objects.get(username=un)
    PO = Profile.objects.get(username=UO)
    d = {'UO':UO, 'PO':PO}
    return render(request,'profile_display.html',d)