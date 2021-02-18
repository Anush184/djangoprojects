from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib.auth import authenticate, login, logout


def create(request):
    return render(request, 'users/create.html')


def register(request):
    form = UserRegisterForm
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.data.get('username')
            password = form.data.get('password1')
            first_name = form.data.get('first_name')
            last_name = form.data.get('last_name')
            user = authenticate(request, username=username, password=password, first_name=first_name, last_name=last_name)
            if user is not None:
                login(request, user)
            return redirect('/home')

    return render(request, "users/register.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect('login/')

