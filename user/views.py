import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from rest_framework_simplejwt.authentication import JWTAuthentication

from skydriver import settings

from .forms import LoginForm, RegisterForm


def sign_up(request):
    if request.method == "GET":
        form = RegisterForm()
        return render(request, "register.html", {"form": form})

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = {
                "username": form.cleaned_data["username"],
                "email": form.cleaned_data["email"],
                "password1": form.cleaned_data["password1"],
                "password2": form.cleaned_data["password2"],
            }
            response = requests.post(f"{settings.API_URL}register/", data=data)
            if response.status_code == 201:
                tokens = response.json()
                request.session["refresh_token"] = tokens["refresh"]
                request.session["access_token"] = tokens["access"]
                messages.success(request, "You have signed up successfully.")
                return redirect("/")

        messages.error(request, "Invalid signup credentials.")
        return render(request, "register.html", {"form": form})


def sign_in(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, "login.html", {"form": form})

    elif request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            data = {"username": cd["username"], "password": cd["password"]}
            response = requests.post(f"{settings.API_URL}token/", data=data)
            if response.status_code == 200:
                request.session["access_token"] = response.json()["access"]
                request.session["refresh_token"] = response.json()["refresh"]
                messages.success(request, "You have signed in successfully.")
                return redirect("/")
            else:
                messages.error(request, "Invalid login credentials.")
                return render(request, "login.html", {"form": form})
    else:
        return render(request, "login.html", {"form": form})


def sign_out(request):
    request.session.pop("refresh_token", None)
    request.session.pop("access_token", None)
    messages.success(request, f"You have been logged out.")
    return redirect("/")
