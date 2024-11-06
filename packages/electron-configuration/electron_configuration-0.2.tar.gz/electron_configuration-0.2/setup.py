from setuptools import setup, find_packages

setup(
    name='electron_configuration',
    version='0.2',  # Update the version with each release
    description='A library to get the electron configuration of elements',
    long_description=open('./README.md').read(),  # The README file is your long description
    long_description_content_type='text/markdown',
    author='Jay Jethwa',
    packages=find_packages(),  # This automatically discovers the electron_configuration package
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Specify the required Python version
    install_requires=[],  # Add external dependencies if necessary
    include_package_data=True,  # Ensure non-Python files are included (e.g., README, LICENSE)
)
