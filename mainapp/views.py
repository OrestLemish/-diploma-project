from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.decorators import login_required
# import paramiko
#
# from apps.server.models import Server


# Create your views here.
class IndexView(View):
    @method_decorator(login_required)
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('servers')
        else:
            return redirect('login')

