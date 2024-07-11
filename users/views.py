from django.shortcuts import render, redirect
from.forms import SignupForm
from.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import BlogPost
from .forms import BlogPostForm
from .models import CATEGORY_CHOICES


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

def home(request):
    return render(request, 'users/home.html')

def create_blog_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user
            blog_post.save()
            return redirect('doctor_dashboard')
    else:
        form = BlogPostForm()
    return render(request, 'users/create_blog_post.html', {'form': form})


def doctor_dashboard(request):
    
    blog_posts = BlogPost.objects.all()
    return render(request, 'users/doctor_dashboard.html', {'blog_posts': blog_posts})

def patient_dashboard(request):
    categories = CATEGORY_CHOICES
    
    blog_posts = BlogPost.objects.filter(is_draft=False)
    return render(request, 'users/patient_dashboard.html', {'categories': categories, 'blog_posts': blog_posts})
