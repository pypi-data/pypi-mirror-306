# netbox/plugins/module_inventory_binder/navigation.py

from netbox.plugins import PluginMenuItem

# Define menu items for the plugin
menu_items = (
    PluginMenuItem(
        link='plugins:module_inventory_binder:binding_list',
        link_text='Module Inventory Bindings',
    ),
)
