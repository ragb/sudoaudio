import glob
import sys, os
from distutils.core import setup


version = "0.2beta1"
packages = ["sudoaudio",
"sudoaudio.speech",
"sudoaudio.speech.drivers",
"sudoaudio.speech.drivers.linux2",
"sudoaudio.speech.drivers.win32"]

extra_kwargs = {}
options = {}

def get_locale_files():
    return glob.glob(os.path.join("sudoaudio", "locale", "*", "LC_MESSAGES", "*"))

def get_puzzle_files():
    return glob.glob(os.path.join("sudoaudio", "puzzles", "*", "*.sudo"))

def get_windows_dlls():
    return glob.glob(os.path.join("sudoaudio", "speech", "drivers", "win32", "*.dll"))

data_files = get_locale_files() + get_puzzle_files() + get_windows_dlls()

# py2exe support
if sys.platform == 'win32':
    import py2exe
    extra_kwargs['zipfile'] = None
    options.update({'py2exe' : {
    'bundle_files' : 3,
    'packages' : ['sudoaudio', 'sudoaudio.speech.drivers.win32', 'pygame'],
    'excludes' : ['Tkinter'],
    'skip_archive' : True,
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
    packages= packages,
    data_files=data_files,
    license='GPL v3',
    long_description=open('README').read(),
    author = "Rui Batista",
    author_email = "ruiandrebatista@gmail.com",
    scripts = ["scripts/sudoaudio"],
    options=options,
    **extra_kwargs
)


