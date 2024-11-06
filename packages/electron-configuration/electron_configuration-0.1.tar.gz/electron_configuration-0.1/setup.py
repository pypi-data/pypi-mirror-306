from setuptools import setup, find_packages

setup(
    name="electron_configuration",
    version="0.1",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "electron-configuration = electron_configuration.main:main",
        ],
    },
    description="A Python package to get the electron configuration of elements, Electron configuration in k,l,m,n format.",
    author="Jay Jethwa",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
