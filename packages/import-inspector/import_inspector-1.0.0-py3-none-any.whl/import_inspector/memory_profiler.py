import importlib
import pympler
from pympler import tracker
import time


def memory_usage_summary(file_path):
    from pympler import muppy, summary

    with open(file_path, "r") as file:
        lines = file.readlines()

    imports = [
        line.split()[1]
        for line in lines
        if line.startswith("import") or line.startswith("from")
    ]

    print("Memory Usage by Module:")
    total_memory = 0
    for module in imports:
        try:
            imported_module = importlib.import_module(module)
            module_size = pympler.asizeof.asizeof(imported_module) / 1024
            total_memory += module_size
            print(f"- {module}: {module_size:.2f} KB")
        except ImportError:
            print(f"Module '{module}' not found.")

    print(f"Total: {total_memory:.2f} KB\n")
