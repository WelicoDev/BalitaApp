from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from .forms import UserCreateForm, ProfileEditForm
from .models import CustomUser

# Create your views here.

class RegisterView(View):
    def get(self, request):
        create_form = UserCreateForm()
        context = {
            "form": create_form,
        }
        return render(request, 'users/register.html', context)

    def post(self, request):
        create_form = UserCreateForm(data=request.POST)

        if create_form.is_valid():
            create_form.save()
            return redirect("users:login")
        else:
            context = {
                "form": create_form,
            }
            return render(request, 'users/register.html', context)


class LoginView(View):
    def get(self, request):
        login_form = AuthenticationForm()
        context = {
            "login_form": login_form,
        }
        return render(request, 'users/login.html', context)

    def post(self, request):
        login_form = AuthenticationForm(data=request.POST)

        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)

            messages.success(request, "You have successfully logged in.")

            return redirect("home")
        else:

            context = {
                "login_form": login_form,
            }
            return render(request, 'users/login.html', context)


class ProfileView(LoginRequiredMixin, View):
    def get(self, request , username):
        user = CustomUser.objects.get(username=username)
        context = {
            "user": user,
        }
        return render(request, 'users/profile.html', context)


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.info(request, "You have successfully logged out.")
        return redirect("https://google.com/")


class ProfileUpdateView(LoginRequiredMixin, View):
    def get(self, request , username):
        user_update_form = ProfileEditForm(instance=request.user)
        context = {
            "form": user_update_form,
        }
        return render(request, 'users/profile_edit.html', context)

    def post(self, request , username):
        user_update_form = ProfileEditForm(instance=request.user, data=request.POST, files=request.FILES)
        context = {
            "form": user_update_form,
        }

        if user_update_form.is_valid():
            user_update_form.save()

            messages.success(request, 'You have successfully updated your profile.')

            return redirect(f"/users/profile/{request.user}/")

        return render(request, 'users/profile_edit.html', context)