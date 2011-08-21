import glob
import sys, os
from setuptools import setup, find_packages, findall


version = "0.2beta1"

extra_kwargs = {}
options = {}

# py2exe support
if sys.platform == 'win32':
    import py2exe
    extra_kwargs['console'] = ['scripts/sudoaudio']
    options.update({'py2exe' : {
    'bundle_files' : 3,
    'zipfile' : None,
    'packages' : ['sudoaudio', 'sudoaudio.speech.drivers.win32', 'pygame'],
    'excludes' : ['Tkinter'],
    }})


    origIsSystemDLL = py2exe.build_exe.isSystemDLL
    def isSystemDLL(pathname):
        dll = os.path.basename(pathname).lower()
        if dll in ("libfreetype-6.dll", "sdl_mixer.dll", "sdl_ttf.dll", "libogg-0.dll", "msvcp71.dll", "msvcp90.dll", "gdiplus.dll","mfc71.dll", "mfc90.dll") or dll.startswith("sdl"):
            return 0
        elif dll.startswith("api-ms-win-") or dll == "powrprof.dll":
            # These are definitely system dlls available on all systems and must be excluded.
            # Including them can cause serious problems when a binary build is run on a different version of Windows.
            return 1
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


