from setuptools import setup, find_packages

setup(
    name='wallid-certishop',
    version='0.1.1',  
    description='A Python library for managing verifiable credentials with WalliD CertiShop.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Filipe Veiga',  
    author_email='info@wallid.io',  
    url='https://github.com/walliDprotocol/CertiShop_lib',  
    packages=find_packages(),
    install_requires=[
        'requests', 
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  
)
