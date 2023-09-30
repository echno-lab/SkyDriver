from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from .forms import LoginForm, RegisterForm


def sign_up(request):
    if request.method == "GET":
        form = RegisterForm()
        return render(request, "register.html", {"form": form})

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, "You have singed up successfully.")
            login(request, user)
            return redirect("/")
        else:
            messages.error(request, "Invalid signup credentials.")
            return render(request, "register.html", {"form": form})


def sign_in(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect("/")

        form = LoginForm()
        return render(request, "login.html", {"form": form})

    elif request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd["username"], password=cd["password"])
            if user is not None:
                login(request, user)
                messages.success(request, "You have logged in successfully.")
                return redirect("/")
            else:
                messages.error(request, "Invalid login credentials.")
                return redirect("login")
        else:
            return render(request, "login.html", {"form": form})


def sign_out(request):
    logout(request)
    messages.success(request, f"You have been logged out.")
    return redirect("login")
