from setuptools import setup, find_packages

setup(
    name='gimmeshell',
    author='Chowdhury Faizal Ahammed',
    description='A comprehensive shell tool for reverse shell operations.',
    entry_points={
        'console_scripts': [
            'gimmeshell=gimmeshell.shell:main',
        ],
    },
    install_requires=[
        'readchar', 'colorama', 'netifaces', 'pyperclip', 'rich'
    ]
)
