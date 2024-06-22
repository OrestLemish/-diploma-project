from django.urls import path, include
from django.contrib import admin

from mainapp.views import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('', include('apps.servers.urls')),
    path('', include('apps.profile.urls')),

]

