from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from posts.models import Post
from django.contrib import messages
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
# Create your views here.

def signup_user(request):
    if request.method=='POST':
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        confirm_password=request.POST.get("confirm_password")

        if password!=confirm_password:
            messages.error(request, 'Password do not match')
            return redirect('/signup/')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('/signup/')
            
        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        messages.success(request, "Account created successfully. Please login.")
        return redirect('/login/')
    
    return render(request,'signup.html')


def login_user(request):
    if request.method=='POST':
        username=request.POST.get("username")
        password=request.POST.get("password")

        user=authenticate(
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            messages.success(request,"Login Sucessful!")
            return redirect("/dashboard/")
        messages.error(request,"Invalid username or password")
        return redirect('/login/')
    
        
    return render(request,"login.html")
    

    
    
@login_required
def dashboard(request):
    posts=Post.objects.filter(author=request.user).order_by('-created_at')
    paginator = Paginator(posts, 5)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)
    return render(request,"dashboard.html",{'posts':posts,'page_obj':page_obj})
    
def logout_user(request):
    logout(request)
    messages.success(request,"Logged Out Sucessfully")
    return redirect("/login/")

