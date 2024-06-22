from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LogoutView, LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View

from apps.profile.forms import RegisterForm


class CustomLoginView(LoginView):
    template_name = "profile/login_page.html"
    redirect_authenticated_user = True
    next_page = "/servers/"


class CustomLogoutView(LogoutView):
    next_page = "/login/"


def AccLoginRedirect(request):
    return redirect('login')


class RegisterView(View):
    def get(self, request):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect("/")

        form = RegisterForm()  # Створення об'єкта форми
        return render(request, 'profile/registration_page.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)

        if form.is_valid():
            profile = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            authenticate(username=username, password=password)
            login(request, profile)
            # user = authenticate(username=profile.username, password=form.cleaned_data['password'])
            return redirect('servers')
        else:
            return render(request, 'profile/registration_page.html', {'form': form})
