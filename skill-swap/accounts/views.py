from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.shortcuts import redirect, render

from SkillSwap.models import Profile
from .forms import LoginForm, RegisterForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = RegisterForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        user = get_user_model().objects.create_user(
            username=form.cleaned_data['username'],
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password'],
        )
        profile = Profile(
            user=user,
            avatar=form.cleaned_data.get('avatar'),
        )
        profile.save()
        login(request, user)
        messages.success(request, 'Регистрация прошла успешно!')
        return redirect('home')

    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        identifier = form.cleaned_data['username_or_email']
        password = form.cleaned_data['password']
        user = authenticate(request, username=identifier, password=password)

        if user is None:
            User = get_user_model()
            candidate = User.objects.filter(email__iexact=identifier).first()
            if candidate:
                user = authenticate(request, username=candidate.get_username(), password=password)

        if user is None:
            form.add_error(None, 'Неверное имя пользователя или пароль.')
        else:
            login(request, user)
            messages.success(request, 'Вы вошли в систему!')
            return redirect('home')

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.info(request, 'Вы вышли из системы.')
    return redirect('home')
