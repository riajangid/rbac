from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Fee, Role

# Register view
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = Role.objects.get(id=request.POST['role_id'])
            user.role = role
            user.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

# Login view
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'users/login.html')

# Logout view
def user_logout(request):
    logout(request)
    return redirect('login')

# Dashboard view
@login_required
def dashboard(request):
    if request.user.is_teacher:
        fees = Fee.objects.all()
        return render(request, 'users/teacher_dashboard.html', {'fees': fees})
    elif request.user.is_student:
        fee_status = Fee.objects.filter(student=request.user)
        return render(request, 'users/student_dashboard.html', {'fee_status': fee_status})

    return redirect('login')
