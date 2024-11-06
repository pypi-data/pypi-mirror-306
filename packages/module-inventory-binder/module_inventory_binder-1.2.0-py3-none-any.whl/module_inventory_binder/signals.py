# netbox/plugins/module_inventory_linker/signals.py

from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from dcim.models import Module
from dcim.models import InventoryItem
from .models import ModuleInventoryLink

@receiver(post_save, sender=Module)
def create_inventory_item_for_module(instance, created, **kwargs):
    """
    Signal triggered after saving a Module instance.
    If the module is newly created, it creates or links to an existing InventoryItem.
    """
    if created:
        # Attempt to find an existing InventoryItem for this module
        existing_inventory = InventoryItem.objects.filter(
            device=instance.device,
            name=f"Inventory for Module {instance.name}"
        ).first()
        if existing_inventory:
            # If it exists, create a binding with the existing item
            ModuleInventoryLink.objects.create(
                module=instance,
                inventory_item=existing_inventory
            )
        else:
            # If not, create a new InventoryItem and bind it to the module
            inventory_item = InventoryItem.objects.create(
                device=instance.device,
                name=f"Inventory for Module {instance.name}",
                item_type='module',  # Ensure 'module' type is defined
                manufacturer=instance.manufacturer,  # If applicable
            )
            ModuleInventoryLink.objects.create(
                module=instance,
                inventory_item=inventory_item
            )

@receiver(pre_delete, sender=Module)
def delete_inventory_item_on_module_delete(instance, **kwargs):
    """
    Signal triggered before deleting a Module instance.
    Deletes the associated InventoryItem if it exists.
    """
    try:
        link = instance.inventory_link
        inventory_item = link.inventory_item
        link.delete()
        inventory_item.delete()
    except ModuleInventoryLink.DoesNotExist:
        pass
