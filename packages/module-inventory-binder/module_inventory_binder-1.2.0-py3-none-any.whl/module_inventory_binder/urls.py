# netbox/plugins/module_inventory_binder/urls.py

from django.urls import path
from . import views

app_name = 'module_inventory_binder'  # Musí odpovídat názvu pluginu

urlpatterns = [
    path('bindings/', views.binding_list, name='binding_list'),
    path('bindings/add/', views.binding_create, name='binding_create'),
    path('bindings/<int:pk>/edit/', views.binding_edit, name='binding_edit'),
    path('bindings/<int:pk>/delete/', views.binding_delete, name='binding_delete'),
]
