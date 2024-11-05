from setuptools import setup, find_packages

setup(
    name='pxndas',  # Name of your package
    version='0.1.0',  # Initial version
    packages=find_packages(),  # Automatically find all sub-packages
    include_package_data=True,  # Include non-Python files specified in MANIFEST.in
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Choose the appropriate license
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
