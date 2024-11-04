from setuptools import setup, find_packages

setup(
    name='curly-brace-python',
    version='0.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[],  # List any dependencies your interpreter needs
    entry_points={
    'console_scripts': [
        'curly-brace-python=brace_interpreter:main',  # Adjust as needed
    ],
},

    description='A custom Python interpreter that allows curly brace syntax',
    author='Komal',
    author_email='h0275141@gmail.com',
    url='https://github.com/komalcantcode/Indentless',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
