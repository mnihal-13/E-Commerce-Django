from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from . models import Customer


def sign_out(request):
    logout(request)
    return redirect('home')
# Create your views here.
def show_account(request):
    # When invalid input get into the login page it will go to the register form
    # To stay on the login page and also showing the message in same login or register page we created a dictionary
    context={}
    # Condition for the request is POST and the Post request is from the register key
    if request.POST and 'register' in request.POST:
        # And set the context value into True when value is in register 
        # This is to which tab is currently active
        context['register']=True 
        try:                
            username=request.POST.get('username')
            password=request.POST.get('password')
            email=request.POST.get('email')
            address=request.POST.get('address')
            phone=request.POST.get('phone')
            
            # creates user accounts
            user=User.objects.create_user(
                username=username,
                password=password,
                email=email
            )
            # creates customer account
            customer=Customer.objects.create(
                name=username,
                user=user,
                phone=phone,
                address=address
            )
            success_message="User registred successfully"
            messages.success(request,success_message)
            
        except Exception as e:
            error_message="Duplicate username or invalid inputs"
            # the message attribute take two argument, so the request parameter want to give
            messages.error(request,error_message)
    if request.POST and 'login' in request.POST: 
        context['register']=False 

        print(request.POST)
        username=request.POST['username']
        password=request.POST['password']
        print(username,password)
        # authenticate is to check if the user is exist of given user-name and password
        user=authenticate(username=username,password=password)
        print(user)
        # If the user is exist login with the user and redirect to home
        if user:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'invalid user credentials')
  
    return render(request,'account.html',context)