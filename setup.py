from setuptools import setup, find_packages

setup(
    name='sudoaudio',
    version='0.1a1pre',
    packages= find_packages(),
    license='GPL v3',
    install_requires = ['pygame'],
    long_description=open('README').read(),
    
    author = "Rui Batista",
    author_email = "ruiandrebatista@gmail.com"
)


