from django.urls import path
from django.contrib.auth.decorators import login_required

from apps.servers.views import ServersView, AddServerView, ServerView, LocationsView, ServerGroupsView, ServerCredentialsView, \
    ModalEditView, ModalDeleteView, ModalAddView, ModalCommandExecute, ModalStandardCommandExecute, CheckServerView

urlpatterns = [
    path('servers/', login_required(ServersView.as_view()), name="servers"),
    path('add_server/', login_required(AddServerView.as_view()), name="add_server"),
    path('server/<path:server_id>/', login_required(ServerView.as_view()), name="server"),
    path('check_server/<int:server_id>/', CheckServerView.as_view(), name="check_server"),

    path('locations/', login_required(LocationsView.as_view()), name="locations"),
    path('groups/', login_required(ServerGroupsView.as_view()), name="groups"),
    path('credentials/', login_required(ServerCredentialsView.as_view()), name="credentials"),

    path('modal_edit_object/<str:model_name>/<int:object_id>/', login_required(ModalEditView.as_view()), name="modal_edit"),
    path('modal_delete_object/<str:model_name>/<int:object_id>/', login_required(ModalDeleteView.as_view()), name="modal_delete"),
    path('modal_add_object/<str:model_name>/', login_required(ModalAddView.as_view()), name="modal_delete"),


    path('modal_command_execute/', login_required(ModalCommandExecute.as_view()), name="modal_command_execute"),
    path('modal_standard_command_execute/', login_required(ModalStandardCommandExecute.as_view()), name="modal_command_execute"),

]
