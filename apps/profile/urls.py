
from django.urls import path

from apps.profile.views import RegisterView, AccLoginRedirect, CustomLoginView, LogoutView, CustomLogoutView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name="login"),
    path('accounts/login/', AccLoginRedirect, name="acc_login"),
    path('logout/', CustomLogoutView.as_view(), name="logout"),
    path('registration/', RegisterView.as_view(), name="registration"),


]
