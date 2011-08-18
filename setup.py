import sys, os
from setuptools import setup, find_packages

extra_kwargs = {}

# py2exe support
if sys.platform == 'win32':
    import py2exe
    extra_kwargs['console'] = ['scripts/sudoaudio']

    origIsSystemDLL = py2exe.build_exe.isSystemDLL
    def isSystemDLL(pathname):
            p = os.path.basename(pathname).lower()
            if p in ("sdl_mixer.dll", "sdl_ttf.dll", "libogg-0.dll") or p.find("sdl") >= 0 or p.find("pygame") >= 0:
                    return 0
            return origIsSystemDLL(pathname)
    py2exe.build_exe.isSystemDLL = isSystemDLL



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



