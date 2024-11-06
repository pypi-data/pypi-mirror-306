# Module Inventory Binder

**Module Inventory Binder** is a plugin for [NetBox](https://github.com/netbox-community/netbox) that facilitates the binding of modules to inventory items. This plugin simplifies the management of relationships between modules and their corresponding inventory items, ensuring better visibility and device management.

## Features

- **One-to-One Binding**: Establish a unique relationship between a module and an inventory item.
- **CRUD Operations**: Create, read, update, and delete bindings between modules and inventory items.
- **Automatic Inventory Item Creation**: Automatically creates or links existing inventory items when new modules are added.
- **Safe Deletion**: Deletes associated inventory items when a module is deleted.
- **Integration with NetBox UI**: Seamlessly integrates into NetBox's main menu for easy access to binding functionalities.

## Requirements

- **NetBox** version `3.0.0` or higher.
- **Python** version `3.10.12` or higher.

## Version 1.1.0
Fixed a an error that occured during pip installation - setup.py configuration had an error in it

## Version 1.2.0
Fixed views.py which used old names for templates

## Version 1.3.0
Fixed problem where deleting binding would end in an error

## Installation with GIT

### Step 1: Clone the Repository into plugins directory in your netbox instance

```bash
git clone https://github.com/vubeckubec/module_inventory_binder.git
```
### Step 2: Add the plugin into PLUGINS in configuration.py

```bash
PLUGINS = [
    'module_inventory_binder',
    # Other plugins...
]
```
### Step 3: Apply migrations(don't forget activating venv)
```bash
python manage.py migrate module_inventory_binder
```
### Step 4: Run netbox(for example)
```bash
python manage.py runserver
```

## Installion with PIP(don't forget activating venv)
This plugin is also available on PYPL so you can install it with PIP
```bash
pip install module_inventory_binder
```

## Troubleshooting tip
If you are encountering an error when creating a new bind with null values you need to manually delete custom field from the ModuleInventoryBinding table here is how to do it. This is an error in current version of the plugin i will try to fix it in the next version.

### Step 1: Open postgres in command line
```bash
sudo -u postgres psql
```

### Step 2: Switch to your DB
```bash
\c your_db_name
```
### Step 3: Delete the custom field
```bash
ALTER TABLE module_inventory_binder_moduleinventorybinding
DROP COLUMN custom_field_data;
```

