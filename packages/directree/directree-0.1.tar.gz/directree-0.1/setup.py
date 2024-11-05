from setuptools import setup, find_packages

setup(
    name='directree',
    version='0.1',
    packages=find_packages(),  # This automatically finds and includes all packages in the directory
    entry_points={
        'console_scripts': [
            'dirtree=dirtree:main',  # This creates a command 'dirtree' that points to the main function
        ],
    },
    install_requires=[],  # Add any dependencies your package may require
    python_requires='>=3.6',  # Specify the minimum Python version required
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
    ],
)
