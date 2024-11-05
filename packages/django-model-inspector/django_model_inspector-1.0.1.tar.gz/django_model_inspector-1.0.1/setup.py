from setuptools import setup, find_packages

setup(
    name='django-model-inspector',    
    version='1.0.1',                   
    packages=find_packages(),
    install_requires=['Django>=3.2'],    
    author='Mowzli Sre Mohan Dass',
    author_email='speak2mowzli@gmail.com',
    description='A utility to inspect Django model schemas',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/mowzlisre/django-model-inspector',  
    classifiers=[
        'Programming Language :: Python :: 3',
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
