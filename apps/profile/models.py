from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.servers.models import Location, ServerGroup, ServerCredential, ServerCommand, Server


class Profile(AbstractUser):
    users_servers = models.ManyToManyField(Server, verbose_name=_("users_servers"), blank=True)
    users_locations = models.ManyToManyField(Location, verbose_name=_("users_locations"), blank=True)
    users_server_group = models.ManyToManyField(ServerGroup, verbose_name=_("users_server_group"), blank=True)
    users_server_credential = models.ManyToManyField(ServerCredential, verbose_name=_("users_server_credential"), blank=True)
    users_server_command = models.ManyToManyField(ServerCommand, verbose_name=_("users_server_command"), blank=True)
    last_interaction = models.DateTimeField(verbose_name=_("last_interaction"), blank=True, null=True)
    # is_busy = models.BooleanField(default=False, verbose_name=_('is_busy'))

