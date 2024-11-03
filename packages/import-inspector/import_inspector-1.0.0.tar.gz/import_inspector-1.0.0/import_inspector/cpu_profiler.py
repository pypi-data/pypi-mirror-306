import importlib
import time


def cpu_usage_summary(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

    imports = [
        line.split()[1]
        for line in lines
        if line.startswith("import") or line.startswith("from")
    ]

    print("CPU Time by Module:")
    total_time = 0
    for module in imports:
        try:
            start_time = time.perf_counter()
            importlib.import_module(module)
            end_time = time.perf_counter()
            module_time = end_time - start_time
            total_time += module_time
            print(f"- {module}: {module_time:.4f}s")
        except ImportError:
            print(f"Module '{module}' not found.")

    print(f"Total Execution Time: {total_time:.4f}s\n")
