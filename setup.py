import sys
from setuptools import setup, find_packages

extra_kwargs = {}

# py2exe support
if sys.platform == 'win32':
    import py2exe
    extra_kwargs['console'] = ['scripts/sudoaudio'],

setup(
    name='sudoaudio',
    version='0.1',
    packages= find_packages(),
    license='GPL v3',
    install_requires = ['pygame'],
    long_description=open('README').read(),
    
    author = "Rui Batista",
    author_email = "ruiandrebatista@gmail.com",
    scripts = ["scripts/sudoaudio"],
    **extra_kwargs
)



