import glob
import os.path

class DriverNotSupportedException(Exception):
    """ Informs that a driver is not supported
    
    Reasons may include libraries not installed or driver doesn't support current platform
    """


class BaseDriver(object):
    def speak(self, message):
        RaiseNotImplementedError
    def cancel(self):
        RaiseNotImplementedError



_registry = None

def _load_registry():
    global _registry
    _registry = []
    basepath = os.path.abspath(os.path.dirname(__file__))
    files = glob.glob(os.path.join(basepath, "*driver.py"))
    modules = [os.path.basename(f)[:-3] for f in files] # strip ".py"
    for module in modules:
        try:
            m = __import__(module, globals=globals())
        except DriverNotSupportedException:
            continue
        try:
            d = m.Driver
            _registry.append(d)
        except AttributeError:
            pass


def list_drivers():
    if _registry is None:
        _load_registry()
    return list(_registry)


