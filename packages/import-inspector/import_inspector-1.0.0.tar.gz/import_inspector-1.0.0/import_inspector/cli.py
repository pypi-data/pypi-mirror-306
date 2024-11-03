import argparse
from import_inspector import memory_profiler, cpu_profiler, detailed_profiler


def main():
    parser = argparse.ArgumentParser(
        description="Analyze import memory and CPU usage of a Python file."
    )
    parser.add_argument("file", help="Path to the Python file to analyze")
    parser.add_argument(
        "--memory", action="store_true", help="Run memory usage analysis"
    )
    parser.add_argument("--cpu", action="store_true", help="Run CPU usage analysis")
    parser.add_argument(
        "--detailed", action="store_true", help="Run detailed profiling"
    )

    args = parser.parse_args()

    if args.memory:
        print("\nRunning Memory Profiler...")
        memory_profiler.memory_usage_summary(args.file)

    if args.cpu:
        print("\nRunning CPU Profiler...")
        cpu_profiler.cpu_usage_summary(args.file)

    if args.detailed:
        print("\nRunning Detailed Profiler...")
        detailed_profiler.detailed_profile(args.file)


if __name__ == "__main__":
    main()
