from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required


# Create your views here.
def signup(request):

    if request.method == "POST":

        username = request.POST['username']

        email=   request.POST['email']
        
        password = request.POST['password']

        confirm_password = request.POST['confirm_password']

        if password == confirm_password:

          User.objects.create_user(username=username,email=email, password=password)

          return redirect('login')
        
        else:
            return render(request,'signup.html',{'error':'passwords do not match'})

    return render(request, 'signup.html')

# LOGIN

def login_view(request):

    if request.method == "POST":

        username = request.POST['username']

        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:

            login(request, user)

            return redirect('profile')

        else:

            return render(request, 'login.html', {"error": "Invalid credentials"})

    return render(request, 'login.html')    
def logout_view(request):
    logout(request)
    return redirect('login')    

def profile(request):
    return render(request,'profile.html')
