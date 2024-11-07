from setuptools import setup, find_packages

setup(
    name='mybit-module',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'asn1crypto==1.5.1',
        'certifi==2024.8.30',
        'cffi==1.17.0',
        'charset-normalizer==3.3.2',
        'coincurve==20.0.0',
        'idna==3.8',
        'pycparser==2.22',
        'requests==2.32.3',
        'urllib3==2.2.2',
    ],
    description='A library for handling multiple cryptocurrencies',
    author='Jhon Doe',
    python_requires='>=3.6',
    package_data={
        'mybit.network': ['servers.json'],  # Incluir el archivo servers.json
    },
)