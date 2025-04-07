from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import auth

from .. import forms

def index(request):
    return render(request, 'pf_index.html')

def login(request):
    form = forms.LoginForm
    if request.method == "POST":
        form = forms.LoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                auth.login(request, user)
                return redirect('index')
    context = {'form':form}
    return render(request, template_name='pf_login.html', context=context)
        
def register(request):
    form = forms.RegisterForm
    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context = {'form':form}
    return render(request, 'pf_register.html', context)

def logout(request):
    auth.logout(request)
    return redirect('index')

def features(request):
    return render(request, 'pf_features.html')

def about(request):
    return render(request, 'pf_about.html')
