from setuptools import setup, find_packages

setup(
    name="import-inspector",
    version="1.0.0",
    author="Saurabh Apraj",
    author_email="saurabhapraj7@gmail.com",
    description="A profiling tool for analyzing memory and CPU usage of Python imports.",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "import-inspector=import_inspector.cli:main",
        ],
    },
    include_package_data=True,
    install_requires=[
        "pympler",
    ],
)
