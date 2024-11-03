# mimodulo/setup.py

from setuptools import setup, find_packages
setup(
    name='mimodulo_sc',
    version='0.1',
    packages=find_packages(),
    description='Un módulo simple para saludar',
    author='Sebastián Cardona',
    author_email='sebascarmun@gmail.com',
    url='https://tuurl.com', # Cambia esto por tu URL si es necesario
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)



