from django import forms
from apps.servers.models import Server, Location, ServerGroup, ServerCredential


# Форма для додавання нових серверів (Отображение, Добавление)

#################### SERVERS ####################
class ServersForm(forms.ModelForm):
    server_change_id = forms.CharField(widget=forms.widgets.HiddenInput(attrs={'id': 'server_change_id'}), required=False)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)

        super().__init__(*args, **kwargs)
        self.fields['server_location'].queryset = user.users_locations
        self.fields['server_group'].queryset = user.users_server_group
        self.fields['server_credentials'].queryset = user.users_server_credential
        self.fields['server_commands'].queryset = user.users_server_command

    class Meta:
        model = Server
        fields = ['name', 'system_name', 'ip_address', 'port', 'packet_name', 'cpu', 'ram', 'price', 'server_location', 'server_group', 'server_credentials', 'server_commands', 'is_active']

    def save(self, commit=True):
        server = super(ServersForm, self).save(commit=False)

        if commit:
            server.save()

        return server


#################### LOCATIONS ####################

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name']

    def save(self, commit=True):
        location = super(LocationForm, self).save(commit=False)

        if commit:
            location.save()

        return location


#################### SERVER GROUPS ####################
class ServerGroupForm(forms.ModelForm):
    class Meta:
        model = ServerGroup
        fields = ['name']

    def save(self, commit=True):
        group = super(ServerGroupForm, self).save(commit=False)

        if commit:
            group.save()

        return group


#################### CREDENTIALS ####################
class ServerCredentialForm(forms.ModelForm):
    class Meta:
        model = ServerCredential
        fields = ['name', 'username', 'password', 'ssh_key']
