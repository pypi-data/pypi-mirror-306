from setuptools import setup, find_packages

setup(
    name="runpy_tool",
    version="1.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "runpy=runpy_tool.runpy:main",
        ],
    },
    author="Your Name",
    description="A command-line tool to run Python scripts with input and output file handling.",
    python_requires=">=3.6",
)