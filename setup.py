# setup.py

from setuptools import setup, find_packages

setup(
    name='darrelops',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask',
        'Flask-SQLAlchemy',
        'Flask-RESTful',
        'requests',
        'typer',
    ],
    entry_points={
        'console_scripts': [
            'darrelops = darrelops.__main__:main',
        ],
    },
)
