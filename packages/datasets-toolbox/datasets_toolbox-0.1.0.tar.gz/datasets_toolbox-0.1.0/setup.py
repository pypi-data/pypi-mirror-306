from setuptools import setup, find_packages

setup(
    name="datasets-toolbox",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "datasets=datasets_toolbox.cli:main",
        ],
    },
)
