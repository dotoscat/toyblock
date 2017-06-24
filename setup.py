from setuptools import setup

setup(
    name='toyblock',
    version='1.3.0',
    description='A pythonic and fast Entity-Component-System written in pure Python',
    long_description=open('README.rst').read(),
    url='https://github.com/dotoscat/toyblock',
    author='Oscar Triano \'dotoscat\'',
    license='LGPL-3.0',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)'
    ],
    keywords='development videogame gamedev',
    packages=['toyblock']
)
