import os.path
import sys

if getattr(sys, "frozen", None):
    # We are running in an executable
    os.chdir(sys.prefix)
    basepath = os.path.abspath('.')
else:
    basepath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

sounds_path = os.path.join(basepath, "sounds")
puzzles_path = os.path.join(basepath, 'puzzles')
localedir = os.path.join(basepath, 'locale')

