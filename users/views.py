from django.shortcuts import render, redirect, reverse, get_object_or_404
from .forms import CreateUserForm, ProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from .models import Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import not_authenticated_user, admin_only, allowed_users


@not_authenticated_user
def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            messages.info(request, "Username or Password is incorrect!")

    context = {}
    return render(request, 'users/login.html', context)


@not_authenticated_user
def register_page(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='customer')
            user.groups.add(group)
            messages.success(request, "Account was created for " + username)
            return redirect('login')

    context = {'form': form}
    return render(request, 'users/register.html', context)


def logout_user(request):
    logout(request)
    return redirect('login')


@login_required
def profile_page(request):
    profile = Profile.objects.get(user=request.user.id)
    return render(request, "users/profile.html", {"profile": profile})


@login_required
def profile_update(request):
    id_ = request.user.id
    user_profile = get_object_or_404(Profile, user=id_)
    form = ProfileForm(instance=user_profile)

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()

            if request.FILES.get('image', None) != None:
                user_profile.image = request.FILES['image']
                user_profile.save()
            messages.success(request, 'Profile was updated successfully!')
        return redirect('profile_page')

    messages.warning(request, 'Profile was not updated successfully!')
    return render(request, "users/profile_update.html", {'form': form})

