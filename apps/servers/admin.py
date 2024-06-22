from django.contrib import admin

from apps.servers.models import Location, ServerGroup, Server, ServerCommand, ServerCredential


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    pass
    # def get_queryset(self, request):
    #     if request.user.is_superuser:
    #         super(LocationAdmin, self).get_queryset(request=request)
    #     return request.user.users_locations


@admin.register(ServerGroup)
class ServerGroupAdmin(admin.ModelAdmin):
    pass
    # def get_queryset(self, request):
    #     if request.user.is_superuser:
    #         super(ServerGroupAdmin, self).get_queryset(request=request)
    #     return request.user.users_server_group


@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    pass
    # def get_queryset(self, request):
    #     if request.user.is_superuser:
    #         super(ServerAdmin, self).get_queryset(request=request)
    #
    #     return request.user.users_servers


@admin.register(ServerCredential)
class ServerCredentialAdmin(admin.ModelAdmin):
    pass
    # def get_queryset(self, request):
    #     if request.user.is_superuser:
    #         super(ServerCredentialAdmin, self).get_queryset(request=request)
    #     return request.user.users_server_credential


@admin.register(ServerCommand)
class ServerCommandAdmin(admin.ModelAdmin):
    pass
    # def get_queryset(self, request):
    #     if request.user.is_superuser:
    #         super(ServerCommandAdmin, self).get_queryset(request=request)
    #     return request.user.users_server_command
