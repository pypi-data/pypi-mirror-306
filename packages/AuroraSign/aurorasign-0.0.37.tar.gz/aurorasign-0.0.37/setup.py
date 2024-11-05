from setuptools import setup, find_packages

setup(
    name="AuroraSign",
    version="0.0.37",
    packages=find_packages(),
    install_requires=[
        'asn1crypto',
        'uritools',
        'oscrypto',
        'tzlocal',
        'pycryptodome'
    ],
)