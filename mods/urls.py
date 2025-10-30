from django.urls import path
from .views import *

urlpatterns = [
    path('', mod_home, name='home'),
    path('details/<int:mod_id>/', mod_detail, name='mod_detail'),
    path('upload/', create_mod, name='create_mod'),
    path('<int:mod_id>/upload-version/', upload_mod_version, name='upload_mod_version'),
    path('<int:mod_id>/edit/', edit_mod, name='edit_mod'),
    path('<int:mod_id>/delete/', delete_mod, name='delete_mod'),
    path('version/<int:version_id>/download/', download_mod_version, name='download_mod_version'),
    path('version/<int:version_id>/edit/', edit_mod_version, name='edit_mod_version'),
    path('version/<int:version_id>/delete/', delete_mod_version, name='delete_mod_version'),
]
