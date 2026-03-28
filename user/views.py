from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest

from .forms import RegisterForm, AuthenticationForm

def register_view(request: HttpRequest):
    if request.method == 'POST':
        form = RegisterForm(data= request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('home')
        
    form = RegisterForm()
        
    context = {
        'form': form
    }
    
    return render(request, 'user/register.html', context)


def login_view(request: HttpRequest):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    form = AuthenticationForm()
    
    context = {
        'form': form
    }
    
    return render(request, 'user/login.html', context)

@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('login')





