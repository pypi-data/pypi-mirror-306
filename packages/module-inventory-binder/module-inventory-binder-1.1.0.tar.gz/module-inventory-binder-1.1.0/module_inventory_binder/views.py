# netbox/plugins/module_inventory_binder/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import permission_required
from django.views.decorators.http import require_http_methods
from .models import ModuleInventoryBinding
from .forms import ModuleInventoryBindingForm

@permission_required('module_inventory_binder.view_moduleinventorybinding')
def binding_list(request):
    """
    View to display a list of all ModuleInventoryBinding records.
    """
    bindings = ModuleInventoryBinding.objects.select_related('module', 'inventory_item').all()
    return render(request, 'module_inventory_binder/binding_list.html', {'bindings': bindings})

@permission_required('module_inventory_binder.add_moduleinventorybinding')
@require_http_methods(["GET", "POST"])
def binding_create(request):
    """
    View to create a new ModuleInventoryBinding record.
    """
    if request.method == 'POST':
        form = ModuleInventoryBindingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('plugins:module_inventory_binder:binding_list'))
    else:
        form = ModuleInventoryBindingForm()
    return render(request, 'module_inventory_binder/binding_form.html', {'form': form, 'action': 'Create'})

@permission_required('module_inventory_binder.change_moduleinventorybinding')
@require_http_methods(["GET", "POST"])
def binding_edit(request, pk):
    """
    View to edit an existing ModuleInventoryBinding record.
    """
    binding = get_object_or_404(ModuleInventoryBinding, pk=pk)
    if request.method == 'POST':
        form = ModuleInventoryBindingForm(request.POST, instance=binding)
        if form.is_valid():
            form.save()
            return redirect(reverse('plugins:module_inventory_binder:binding_list'))
    else:
        form = ModuleInventoryBindingForm(instance=binding)
    return render(request, 'module_inventory_binder/binding_form.html', {'form': form, 'action': 'Edit'})

@permission_required('module_inventory_binder.delete_moduleinventorybinding')
@require_http_methods(["POST"])
def binding_delete(pk):
    """
    View to delete an existing ModuleInventoryBinding record.
    """
    binding = get_object_or_404(ModuleInventoryBinding, pk=pk)
    binding.delete()
    return redirect(reverse('plugins:module_inventory_binder:binding_list'))
