from setuptools import find_packages, setup

setup(
    name="pyodide_app",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    author="Jules",
    author_email="jules@example.com",
    description="A simple Pyodide application.",
)
