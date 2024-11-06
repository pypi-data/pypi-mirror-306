# netbox/plugins/module_inventory_binder/admin.py

from django.contrib import admin
from .models import ModuleInventoryBinding
from dcim.models import Module
from dcim.admin import ModuleAdmin as BaseModuleAdmin

class ModuleInventoryBindingInline(admin.StackedInline):
    model = ModuleInventoryBinding
    can_delete = True
    verbose_name = "Module Inventory Binding"
    verbose_name_plural = "Module Inventory Bindings"
    fk_name = 'module'

@admin.register(ModuleInventoryBinding)
class ModuleInventoryBindingAdmin(admin.ModelAdmin):
    list_display = ('module', 'inventory_item')
    search_fields = ('module__name', 'inventory_item__name')
    list_filter = ('module__device', 'inventory_item__item_type')

# Odregistrování původního ModuleAdmin, pokud je registrován
try:
    admin.site.unregister(Module)
except admin.sites.NotRegistered:
    pass

@admin.register(Module)
class CustomModuleAdmin(BaseModuleAdmin):
    inlines = BaseModuleAdmin.inlines + [ModuleInventoryBindingInline]
