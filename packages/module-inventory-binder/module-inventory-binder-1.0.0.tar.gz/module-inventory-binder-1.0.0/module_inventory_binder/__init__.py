from netbox.plugins import PluginConfig
from django.urls import path, include

class ModuleInventoryBinderConfig(PluginConfig):
    name = 'module_inventory_binder'
    verbose_name = 'Module Inventory Binder'
    description = 'Plugin to manually bind modules with inventory items.'
    version = '1.0.0'
    author = 'Viktor Kubec'
    author_email = 'Viktor.Kubec@gmail.com'
    base_url = 'module-inventory-binder'
    required_settings = []
    default_settings = {}

config = ModuleInventoryBinderConfig
