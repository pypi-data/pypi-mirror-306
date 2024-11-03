import os
import importlib
import pkgutil
from typing import List

from ..toolkit.paths import TOOLKIT_ROOT


class Extension(object):
    """Base class for extensions.

    Extensions are registered with the ExtensionManager, which is
    responsible for calling the extension's load() and unload()
    methods at the appropriate times.

    """

    name: str = None
    uid: str = None

    @classmethod
    def get_process(cls):
        # extend in subclass
        pass


def get_all_extensions() -> List[Extension]:
    extension_folders = ['extensions', 'extensions_built_in']
    package_dir = ['ostris_ai_toolkit.extensions', 'ostris_ai_toolkit.extensions_built_in']

    # This will hold the classes from all extension modules
    all_extension_classes: List[Extension] = []

    # Iterate over all directories (i.e., packages) in the "extensions" directory
    for i, sub_dir in enumerate(extension_folders):
        extensions_dir = os.path.join(TOOLKIT_ROOT, sub_dir)
        print(f"extensions_dir: {extensions_dir}")
        for (_, name, _) in pkgutil.iter_modules([extensions_dir]):
            try:
                # Import the module
                module = importlib.import_module(f"{package_dir[i]}.{name}")
                extensions = getattr(module, "AI_TOOLKIT_EXTENSIONS", None)
                # Check if the value is a list
                if isinstance(extensions, list):
                    # Iterate over the list and add the classes to the main list
                    all_extension_classes.extend(extensions)
            except ImportError as e:
                print(f"Failed to import the {name} module. Error: {str(e)}")

    return all_extension_classes


def get_all_extensions_process_dict():
    all_extensions = get_all_extensions()
    process_dict = {}
    for extension in all_extensions:
        process_dict[extension.uid] = extension.get_process()
    return process_dict
