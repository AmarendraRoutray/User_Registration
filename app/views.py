from django.shortcuts import render

# Create your views here.
from .forms import *
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import random

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
            messages.success(request,'Logged In')
            return HttpResponseRedirect(reverse('home'))
    
    return render(request,'user_login.html')



@login_required
def user_logout(request):
    logout(request)
    messages.success(request,'Logged Out')
    return HttpResponseRedirect(reverse('home'))


@login_required
def profile_display(request):
    un = request.session.get('username')
    UO = User.objects.get(username=un)
    PO = Profile.objects.get(username=UO)
    d = {'UO':UO, 'PO':PO}
    return render(request,'profile_display.html',d)



def generate_otp():
    return ''.join(random.choices('0123456',k=4))


def verify_otp(request):
    if request.method=='POST':
        entered_otp=request.POST.get('otp')
        
        #change password
        if 'change_password_otp' in request.session:
            change_stored_otp=request.session.get('change_password_otp')
            change_password = request.session.get('change_password')
            change_password_user = request.session.get('change_password_user')
            change_UO = User.objects.get(username=change_password_user)
            
            if change_stored_otp==entered_otp:
                change_UO.set_password(change_password)
                change_UO.save()
                #deleting from session
                del request.session['change_password']
                del request.session['change_password_otp']
                
                messages.success(request,'Password Changed successfully')
                return HttpResponseRedirect(reverse('user_login'))
            else:
                messages.warning(request,'Invalid OTP')
                return HttpResponseRedirect(reverse('verify_otp'))
        
        #forgot password
        elif 'forgot_password_otp' in request.session:
            forgot_stored_otp=request.session.get('forgot_password_otp')
            forgot_password=request.session.get('forgot_password')
            forgot_password_user=request.session.get('forgot_password_user')
            forgot_UO=User.objects.get(username=forgot_password_user)
        
            if forgot_stored_otp==entered_otp:
                forgot_UO.set_password(forgot_password)
                forgot_UO.save()
                # deleting from session
                del request.session['forgot_password']
                del request.session['forgot_password_otp']
                
                messages.success(request,'Password Reset successfull')
                return HttpResponseRedirect(reverse('user_login'))
            else:
                messages.warning(request,'Invalid OTP')
                return HttpResponseRedirect(reverse('verify_otp'))
        else:
            messages.warning(request,'Invalid OTP')
            return HttpResponseRedirect(reverse('verify_otp'))
        
    return render(request,'verify_otp.html')



def change_password(request):
    if request.method=='POST':
        pw=request.POST['pw']
        email=request.POST['email']
        un=request.session.get('username')
        UO=User.objects.get(username=un)

        otp=generate_otp()
        
        send_mail(
            'OTP for changing password',
            f'Otp for changing password {otp}',
            'amarendraroutray6@gmail.com',
            [email],
            fail_silently=True
        )
        
        request.session['change_password']=pw
        
        request.session['change_password_otp']=otp
        request.session['change_password_user']=UO.username
        
        return HttpResponseRedirect(reverse('verify_otp'))
        
        
        # return HttpResponse('Password changed successfully')
    return render(request,'change_password.html')


def forgot_password(request):
    if request.method=='POST':
        username=request.POST['un']
        password=request.POST['pw']
        email=request.POST['email']
        LUO=User.objects.filter(username=username)
        
        if LUO:
            UO=LUO[0]
            
            otp=generate_otp()
        
            send_mail(
            'OTP for resetting password',
            f'Otp for reset password : {otp}',
            'amarendraroutray6@gmail.com',
            [email],
            fail_silently=True
            )
            
            request.session['forgot_password']=password
            request.session['forgot_password_otp']=otp
            request.session['forgot_password_user']=UO.username
            
            return HttpResponseRedirect(reverse('verify_otp'))
            # return HttpResponse('Password reset successfull')
        else:
            return HttpResponse('Username not available')
        
    return render(request,'forgot_password.html')



