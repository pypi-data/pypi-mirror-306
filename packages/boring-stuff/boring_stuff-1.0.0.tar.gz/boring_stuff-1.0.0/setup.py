from setuptools import setup, find_packages

setup(
    name="boring-stuff",
    version="1.0.0",
    author="Saurabh Apraj",
    author_email="saurabhapraj7@gmail.com",
    description="A package that will help Developer's to setup project.",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "boring-stuff=boring_stuff.cli:main",
        ],
    },
    include_package_data=True,
    install_requires=[],
)
