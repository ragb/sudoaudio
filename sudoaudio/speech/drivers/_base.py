# Copyright (c) 2011 - Rui Batista <ruiandrebatista@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


import glob
import logging
import os.path


logger = logging.getLogger(__name__)

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
    logger.info("loading speech drivers")
    _registry = []
    basepath = os.path.abspath(os.path.dirname(__file__))
    files = glob.glob(os.path.join(basepath, "*driver.py"))
    modules = [os.path.basename(f)[:-3] for f in files] # strip ".py"
    for module in modules:
        try:
            logger.info("Trying to import module %s", module)
            m = __import__(module, globals=globals())
        except DriverNotSupportedException:
            logger.info("Module can not be imported")
            continue
        try:
            d = m.Driver
            _registry.append(d)
        except AttributeError:
            logger.error("module %s does not contain a driver class", m.__name__)
        if not _registry:
            logger.critical("No drivers loaded")
            return False
        return True

def list_drivers():
    if _registry is None:
        _load_registry()
    return list(_registry)


