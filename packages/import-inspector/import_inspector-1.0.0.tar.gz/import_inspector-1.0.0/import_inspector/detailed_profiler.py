import importlib
import tracemalloc


def detailed_profile(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

    imports = [
        line.split()[1]
        for line in lines
        if line.startswith("import") or line.startswith("from")
    ]

    tracemalloc.start()

    print("Detailed Memory Usage by Module:")
    for module in imports:
        try:
            importlib.import_module(module)
        except ImportError:
            print(f"Module '{module}' not found.")

    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics("lineno")

    for stat in top_stats[:10]:  # Top 10 lines by memory consumption
        print(stat)

    tracemalloc.stop()
