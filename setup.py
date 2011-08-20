import sys, os
from setuptools import setup, find_packages

version = "0.2beta1"

extra_kwargs = {}
options = {}

# py2exe support
if sys.platform == 'win32':
    import py2exe
    extra_kwargs['console'] = ['scripts/sudoaudio']
    options.update({'py2exe' : {
    'bundle_files' : 2,
    'packages' : 'sudoaudio'
    }})



    origIsSystemDLL = py2exe.build_exe.isSystemDLL
    def isSystemDLL(pathname):
            p = os.path.basename(pathname).lower()
            if p in ("sdl_mixer.dll", "sdl_ttf.dll", "libogg-0.dll") or p.find("sdl") >= 0 or p.find("pygame") >= 0:
                    return 0
            return origIsSystemDLL(pathname)
    py2exe.build_exe.isSystemDLL = isSystemDLL



setup(
    name='sudoaudio',
    version=version,
    packages= find_packages(),
    license='GPL v3',
    install_requires = ['pygame'],
    long_description=open('README').read(),
    author = "Rui Batista",
    author_email = "ruiandrebatista@gmail.com",
    scripts = ["scripts/sudoaudio"],
    options=options,
    **extra_kwargs
)



