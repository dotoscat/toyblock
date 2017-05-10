from setuptools import setup

setup(
    name='toyblock',
    version='1.0.0',
    description='A pythonic and fast Entity-Component-System written in pure Python',
    long_description=open('README.rst').read(),
    url='https://github.com/dotoscat/toyblock',
    author='Oscar Triano \'dotoscat\'',
    license='GPL-3.0',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries'
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)'
    ],
    keywords='development videogame gamedev',
    packages=['toyblock']
)
