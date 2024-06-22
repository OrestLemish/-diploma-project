import re

from django.http import JsonResponse
from django.shortcuts import render, redirect

from django.views import View
from django.apps import apps
from apps.servers.forms import ServersForm, LocationForm, ServerGroupForm, ServerCredentialForm  # не видаляти

######################################################### Створення Вюшки для показу сторінки з серверами
from apps.servers.models import Server, Location, ServerGroup, ServerCredential  # не видаляти
from mainapp.globals import SERVER_COMMANDS


class ServersView(View):

    def get(self, request):
        servers = request.user.users_servers.all()
        return render(request, 'servers/servers_page.html', {'servers': servers})


class ServerView(View):
    server_id = None

    def get(self, request, server_id):
        server = Server.objects.get(id=server_id)
        form = ServersForm(user=request.user, instance=server)
        commands_list = SERVER_COMMANDS[server.system_name]
        return render(request, 'servers/server_detail.html', {'server': server, "form": form, "commands_list": commands_list})


# Вьюшка для додавання нового серверу
class AddServerView(View):

    # Дії отримання форми
    def get(self, request):
        form = ServersForm(user=request.user)
        return render(request, 'servers/add_server.html', {'form': form})

    # Сохраняє сервери, принімає сигнали з форми
    def post(self, request):
        form = ServersForm(request.POST, user=request.user)

        if form.is_valid():
            # Збереження сервера
            server = form.save(commit=False)
            server.save()
            request.user.users_servers.add(server)
            request.user.save()

            return redirect('servers')
        else:
            return render(request, 'servers/add_server.html', {'form': form})


# class ServerCommandView(View):
#     def get(self, request, server_id, credential_id):
#         server = Server.objects.get(id=server_id)
#         response = server.connect_server(credential_id)
#         res = {'success': True, "recponse": response}
#         return JsonResponse(res)


######################################################### Локации
class LocationsView(View):
    def get(self, request):
        locations = request.user.users_locations.all()
        return render(request, 'servers/objects_page.html', {'objects': locations, "model_name": "Location"})


######################################################### Групи для серверів
class ServerGroupsView(View):
    def get(self, request):
        groups = request.user.users_server_group.all()
        return render(request, 'servers/objects_page.html', {'objects': groups, "model_name": "ServerGroup"})


######################################################### Дані авторизації
class ServerCredentialsView(View):
    def get(self, request):
        credentials = request.user.users_server_credential.all()
        return render(request, 'servers/objects_page.html', {'objects': credentials, "model_name": "ServerCredential"})


class ModalEditView(View):

    # Дії отримання форми
    def get(self, request, model_name, object_id):

        model = apps.get_model(app_label='servers', model_name=model_name)
        model_object = model.objects.get(id=object_id)
        form = None
        if model_name in globals():
            form_class = globals()[f"{model_name}Form"]
            form = form_class(instance=model_object)

        return render(request, 'servers/includes/modals/modal_edit_item.html', {'form': form, 'object_id': object_id, 'model_name': model_name})

    def post(self, request, model_name, object_id):
        model = apps.get_model(app_label='servers', model_name=model_name)
        model_object = model.objects.get(id=object_id)
        form = None
        if model_name in globals():
            form_class = globals()[f"{model_name}Form"]
            form = form_class(request.POST, instance=model_object)

        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})


class ModalDeleteView(View):

    # Дії отримання форми
    def get(self, request, model_name, object_id):
        return render(request, 'servers/includes/modals/modal_delete_item.html', {'object_id': object_id, 'model_name': model_name})

    def post(self, request, model_name, object_id):
        model = apps.get_model(app_label='servers', model_name=model_name)
        model_object = model.objects.get(id=object_id)
        model_object.delete()
        return JsonResponse({'success': True})


class ModalAddView(View):

    # Дії отримання форми
    def get(self, request, model_name):
        form = None
        if f"{model_name}Form" in globals():
            form_class = globals()[f"{model_name}Form"]
            form = form_class(request.POST)
        print(form)
        return render(request, 'servers/includes/modals/modal_add_item.html', {'form': form, 'model_name': model_name})

    # Сохраняє сервери, принімає сигнали з форми
    def post(self, request, model_name):

        form = None
        if model_name in globals():
            form_class = globals()[f"{model_name}Form"]
            form = form_class(request.POST)

        if form.is_valid():
            modal_object = form.save()
            if model_name == "Location":
                request.user.users_locations.add(modal_object)
            if model_name == "ServerGroup":
                request.user.users_server_group.add(modal_object)
            if model_name == "ServerCredential":
                request.user.users_server_credential.add(modal_object)
            request.user.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})


class ModalCommandExecute(View):

    # Дії отримання форми
    def get(self, request):
        command_text = request.GET["command_text"]
        return render(request, 'servers/includes/modals/modal_exec_serv_command.html', {'command_text': command_text})

    def post(self, request):
        command_text = request.POST["command_text"]
        server_id = request.POST["server_id"]
        server = Server.objects.get(id=server_id)
        response = server.execute_comand(4, command_text)
        res = {'success': True, "response": response}
        return JsonResponse(res)


class ModalStandardCommandExecute(View):

    # Дії отримання форми
    def get(self, request):
        command_text = request.GET["command_text"]
        missing_arguments = set(re.findall(r'#(.*?)#', command_text))
        hint = re.findall(r'\?(.*?)\?', command_text)
        if hint:
            hint = hint[0]
        return render(request, 'servers/includes/modals/modal_exec_standard_serv_command.html',
                      {'command_text': command_text, "missing_arguments": missing_arguments, "hint": hint})


class CheckServerView(View):

    # Дії отримання форми
    def post(self, request, server_id):
        data = {}
        if server_id != 0:
            server = Server.objects.get(id=server_id)
            data[server.name] = server.ping_server()
        else:
            for server in request.user.users_servers.all():
                data[server.name] = server.ping_server()
        print(data)
        return JsonResponse({'success': True, "data": data})
