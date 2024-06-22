from django.contrib import admin

from apps.profile.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
   pass



