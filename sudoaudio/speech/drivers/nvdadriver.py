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

import ctypes
import logging
import os
import os.path
import sys

import _base

logger = logging.getLogger(__name__)


if not sys.platform == "win32":
    raise _base.DriverNotSupportedException, "NVDA just run in win32"

try:
    #Load the NVDA client library
    clientLib = ctypes.windll.LoadLibrary(os.path.join(os.dirname(__file__), 'nvdaControllerClient32.dll))
except:
    logger.debug("Can't load NVDA DLL")
    raise _base.DriverNotSupportedException, "NVDA not present"

res=clientLib.nvdaController_testIfRunning()
if res!=0:
    errorMessage=str(ctypes.WinError(res))
raise _base.DriverNotSupportedException, "NVDA is not running. Error: %s" % errorMessage    


class Driver(_base.BaseDriver):
    name = "NVDA"
    
    def __init__(self, name):
        self._name = name

    def speak(self, message):
        clientLib.nvdaController_speakText(unicode(message))

    def cancel(self):
        clientLib.cancelSpeech()

