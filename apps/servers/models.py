import os
import subprocess

import paramiko
from django.contrib.auth.models import User
from django.db import models
from django.http import request
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# Create your models here.
from django.core.validators import MinValueValidator, MaxValueValidator

from django_currentuser.middleware import get_current_user
from mainapp.globals import SYSTEMS_VARIANTS
from unine_engine import settings


# Розташування країна
class Location(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Country'))

    def __str__(self):
        return self.name


# Серверна група(DO,Hetzner,AWS,other)
class ServerGroup(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Group'))

    def __str__(self):
        return self.name


def user_ssh_key_path(instance, filename):
    user = get_current_user()
    # instance - це екземпляр моделі ServerCredential, filename - ім'я файлу
    # Визначаємо папку користувача на основі його імені
    user_folder = os.path.join(settings.MEDIA_ROOT, user.username)
    # Повний шлях до папки, де ми хочемо зберегти файл
    upload_path = os.path.join('ssh_keys', user_folder)
    # Повертаємо шлях, де файл повинен бути збережений
    return upload_path + '/' + filename


class ServerCredential(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name_credential'))
    username = models.CharField(max_length=255, verbose_name=_('Login'))
    password = models.CharField(max_length=255, blank=True, null=True, default=None, verbose_name=_('Password'))
    ssh_key = models.FileField(upload_to=user_ssh_key_path, blank=True, null=True, max_length=255, default="", verbose_name=_('SSH_key'))

    def save(self, *args, **kwargs):
        # user = get_current_user()
        # user_folder = os.path.join(settings.MEDIA_ROOT, user.username)
        # if not os.path.exists(user_folder):
        #     os.makedirs(user_folder)
        #
        # ssh_key = self.ssh_key
        # if ssh_key:
        #     # Создаем путь к файлу в папке пользователя
        #     file_path = os.path.join(user_folder, ssh_key.name)
        #
        #     # Загружаем файл в папку пользователя
        #     with open(file_path, 'wb') as destination:
        #         for chunk in ssh_key.chunks():
        #             destination.write(chunk)

        # # Устанавливаем путь к файлу в поле ssh_key модели
        # self.ssh_key.name = os.path.join(user.username, ssh_key.name)

        super(ServerCredential, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class ServerCommand(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Command_name"))
    command = models.TextField(verbose_name=_('Server_command_text'), blank=True, null=True)

    def __str__(self):
        return self.name


class ServerDisk(models.Model):
    disk_maximum_space = models.FloatField(max_length=255, blank=True, null=True, default=None, verbose_name=_('Disk_size'))
    disk_occupied_space = models.FloatField(max_length=255, blank=True, null=True, default=None, verbose_name=_('Disk_size'))
    path = models.CharField(max_length=255, blank=True, null=True, default=None, verbose_name=_('Disk_path'))


# Cервер, айпі, порт, розташування, серверна група, технічні характеристики, якими даними авторизуємось
class Server(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True, default=None, verbose_name=_('Server_name'))
    system_name = models.CharField(max_length=255, choices=SYSTEMS_VARIANTS, blank=True, null=True, default=None, verbose_name=_('System_name'))
    ip_address = models.GenericIPAddressField(blank=True, null=True, default=None, verbose_name=_('IP_address'))
    port = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(65535)], blank=True, null=True, default=None, verbose_name=_('Port'))

    server_location = models.ForeignKey(Location, on_delete=models.CASCADE, blank=True, null=True, default=None, verbose_name=_('Location'))
    server_group = models.ForeignKey(ServerGroup, on_delete=models.CASCADE, blank=True, null=True, default=None, verbose_name=_('Server_group'))
    server_commands = models.ManyToManyField(ServerCommand, blank=True, null=True, default=None, verbose_name=_('Server_command'))
    server_credentials = models.ManyToManyField(ServerCredential, blank=True, verbose_name=_('Credentials'))
    server_disks = models.ManyToManyField(ServerDisk, blank=True, verbose_name=_('Server_disk'))

    packet_name = models.CharField(max_length=255, verbose_name=_('Packet_name'))
    cpu = models.CharField(max_length=255, blank=True, null=True, default=None, verbose_name=_('CPU'))
    ram = models.CharField(max_length=255, blank=True, null=True, default=None, verbose_name=_('RAM'))
    price = models.DecimalField(max_digits=10, blank=True, null=True, default=None, decimal_places=2, verbose_name=_('Monthly_payment'))

    # Поле активності серверу, оновлення раз 30 хв, за замовуванням та простий пінг на сервер
    is_active = models.BooleanField(default=True, verbose_name=_('Status'))



    # Поле вибору якими даними авторизуємось

    @property
    def total_disk_space(self):
        server_disks = self.server_disks.all()
        total_space = sum(server_disk.disk_maximum_space for server_disk in server_disks)

        return total_space

    def get_absolute_url(self):
        return reverse('server', args=[str(self.id)])

    def ping_server(self):
        try:
            result = subprocess.call(["ping", "-n", "1", self.ip_address])

            if result == 0:
                self.is_active = True
                self.save()
                return True
            else:
                self.is_active = False
                self.save()
                return False

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return False

    def execute_comand(self, credential_id, command_text):
        ip_server = self.ip_address
        port = self.port

        credential = self.server_credentials.get(id=credential_id)

        name = credential.username
        password = credential.password

        ssh = paramiko.SSHClient()

        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            if credential.ssh_key:
                key_filename = f"media/{credential.ssh_key}"
                ssh.connect(ip_server, port=port, username=name, key_filename=key_filename)

            else:

                ssh.connect(ip_server, port=port, username=name, password=password)

        except:
            ssh = None
        stdin, stdout, stderr = ssh.exec_command(command_text)
        output = stdout.read().decode('utf-8')
        ssh.close()
        return output
