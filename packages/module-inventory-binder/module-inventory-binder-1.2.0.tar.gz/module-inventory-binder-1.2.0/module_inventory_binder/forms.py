# netbox/plugins/module_inventory_binder/forms.py

from django import forms
from .models import ModuleInventoryBinding


class ModuleInventoryBindingForm(forms.ModelForm):
    """
    Form for creating and updating ModuleInventoryBinding records.
    Includes fields for selecting a module and an inventory item.
    """
    class Meta:
        model = ModuleInventoryBinding
        fields = ['module', 'inventory_item']
        widgets = {
            'module': forms.Select(attrs={'class': 'form-control'}),
            'inventory_item': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        """
        Clean and validate the form data.
        Ensures that the module and inventory item are not already bound to other records.
        """
        cleaned_data = super().clean()
        module = cleaned_data.get('module')
        inventory_item = cleaned_data.get('inventory_item')

        # Check if the module is already bound to another inventory item
        if ModuleInventoryBinding.objects.filter(module=module).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(f"Module '{module}' je již svázán s Inventářní položkou.")

        # Check if the inventory item is already bound to another module
        if ModuleInventoryBinding.objects.filter(inventory_item=inventory_item).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(f"Inventářní položka '{inventory_item}' je již svázána s Modulem.")

        return cleaned_data
