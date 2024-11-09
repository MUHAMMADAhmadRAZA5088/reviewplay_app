from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
User = get_user_model()  # Get the custom user model

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2:
            try:
                user = User.objects.create_user(username=username, email=email, password=password1)  # Set to False for admin approval
                user.save()
                return redirect('login')  
            except Exception as e:
                messages.error(request, f'Error creating account: {str(e)}')
        else:
            messages.error(request, 'Passwords do not match.')
    
    return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['name']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # Built-in Django login function
            return redirect('home')  # Redirect to home or another page
          
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')

def logout_view(request):
    request.session.flush()
    logout(request)  # This will clear the session
    return redirect('login')  # Redirect to login page after logout


@login_required
def home(request):
    return render(request, 'home.html')

