# netbox/plugins/module_inventory_binder/models.py

from django.db import models
from dcim.models import Module
from dcim.models import InventoryItem

class ModuleInventoryBinding(models.Model):
    """
    Model to bind a Module to an Inventory Item.
    This model allows a one-to-one relationship between a module and an inventory item.
    """
    module = models.OneToOneField(
        Module,
        on_delete=models.CASCADE,
        related_name='inventory_binding',
        help_text="The module linked to an inventory item."
    )
    inventory_item = models.OneToOneField(
        InventoryItem,
        on_delete=models.CASCADE,
        related_name='module_binding',
        help_text="The inventory item linked to a module."
    )

    class Meta:
        verbose_name = "Module Inventory Binding"
        verbose_name_plural = "Module Inventory Bindings"

    def __str__(self):
        """
        String representation of the ModuleInventoryBinding instance.
        """
        return f"Module {self.module} linked to Inventory Item {self.inventory_item}"
