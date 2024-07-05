from django.shortcuts import render, redirect
from.forms import SignupForm
from.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            print("Form is valid")
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.is_active = True
            print(user)
            try:
                user.save()
                print("User saved successfully")
            except Exception as e:
                print(f"Error saving user: {e}")
            return redirect('login')
        else:
            print("Form is not valid")
            print(form.errors)
    else:
        form = SignupForm()
    return render(request, 'users/signup.html', {'form': form})
def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        print(f"Email: {email}, Password: {password}")
        user = authenticate(username=email, password=password)
        print(f"Authenticated user: {user}")
        if user is not None:
            print("User is authenticated")
            login(request, user)
            print(f"User type: {user.user_type}")
            if user.user_type == 'Doctor':
                return redirect('doctor_dashboard')
            elif user.user_type == 'Patient':
                return redirect('patient_dashboard')
        else:
            print("Not logged In")
    return render(request, 'users/login.html')
def doctor_dashboard(request):
    user = request.user
    return render(request, 'users/doctor_dashboard.html', {'user': user})

def patient_dashboard(request):
    user = request.user
    return render(request, 'users/patient_dashboard.html', {'user': user})

def home(request):
    return render(request, 'users/home.html')