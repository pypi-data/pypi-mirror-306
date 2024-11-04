import importlib


def get_module_exports(module_name, as_dict=False):
    """
    Get exports from a module as objects.

    :param module_name: Name of the module to import from.
    :param as_dict: If True, return a dictionary of name-object pairs. If False, return a list of objects.
    :return: List of exported objects or dictionary of name-object pairs from the module.
    """
    # Import the module
    module = importlib.import_module(module_name)

    # Get all names defined in the module
    all_names = dir(module)

    # Filter out names that start with underscore (considered private)
    exports = {name: getattr(module, name)
               for name in all_names if not name.startswith('_')}

    # If the module defines __all__, use that instead
    if hasattr(module, '__all__'):
        exports = {name: getattr(module, name) for name in module.__all__}

    if as_dict:
        return exports
    else:
        return list(exports.values())
