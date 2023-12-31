from django.shortcuts import render
from django.contrib.auth import login as auth_login, logout
from admin_dash.models import User
from django.contrib import messages
from django.shortcuts import render, HttpResponse, redirect



def sign_out(request):
    logout(request)
    messages.success(request, 'Log out Successfully!')
    return redirect('login')

from django.contrib.auth import authenticate
# from django.shortcuts import render, redirect

# def admin_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         # Authenticate the user
#         user = authenticate(username=username, password=password)

#         if user is not None and user.is_superuser:
#             # Log in the user (admin)
#             auth_login(request, user)
#             return redirect('admin-dashboard')  # Replace 'admin_dashboard' with your admin page URL
#         elif user is not None and user.is_superuser:
#             # Handle invalid login credentials
#             # ...

#     return render(request, 'admin_login.html')


def login(request):
    if request.POST:
        password = request.POST['password']
        username = request.POST['username']
        
        user = authenticate(username=username, password=password)
        print(user)
        if user is None:
            user = User.objects.filter(username=username, password=password).first()
        print(user)
        
        if user is not None and user.is_superuser:
            auth_login(request, user)
            messages.success(request, 'Log In Successfully!')
            return redirect('admin-dashboard')
        elif user is not None and not user.is_superuser:
            auth_login(request, user)
            messages.success(request, 'Log In Successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Bad Credential!')
        
        # if User.objects.filter(email=email, password=password).exists():
        #     user = User.objects.get(email=email, password=password)
        #     auth_login(request, user)
        #     messages.success(request, 'Log In Successfully!')
            
        #     next_url = request.GET.get('next')
        #     if next_url:
        #         return redirect(next_url)
        #     return redirect('dashboard')
        # else:
        #     messages.error(request, 'Bad Credential!')

    return render(request, 'authentication/login.html')


def signup(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exist')
            return redirect('signup')
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already exist")
            return redirect('signup')
        elif len(password)<8:
            messages.error(request, "Password must be 8 characters")
            return redirect('signup')
        user = User.objects.create(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
        user.mobile = request.POST['mobile']
        user.address = request.POST['address']
        user.nid_or_birth = request.FILES['nid_or_birth']
        user.save()
        auth_login(request, user)

        return redirect("dashboard")
        
    return render(request, 'authentication/register.html')
    
# Create your views here.
