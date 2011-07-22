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

import logging

import _base

logger = logging.getLogger(__name__)

try:
    import comtypes.client
    from comtypes import COMError
    import _winreg
except ImportError:
    raise _base.DriverNotSupportedException, "Comm modules not present"

COM_CLASS = "SAPI.SPVoice"

try:
	r=_winreg.OpenKey(_winreg.HKEY_CLASSES_ROOT,COM_CLASS)
	r.Close()
	logger.debug("SAPI5 is present")
except:
	logger.debug("SAPI% not present")
	raise _base.DriverNotSupportedException, "SAPI5 is not Installed"



class constants:
	SVSFlagsAsync = 1
	SVSFPurgeBeforeSpeak = 2
	SVSFIsXML = 8


class Driver(_base.BaseDriver):
	name ="SAPI5"

	def __init__(self, name):
		super(Driver, self).__init__()
		self.tts=comtypes.client.CreateObject(COM_CLASS)

	def speak(self, message):
		self.tts.speak(message, constants.SVSFlagsAsync)

	def cancel(self):
		self.tts.Speak(None, constants.SVSFlagsAsync | constants.SVSFPurgeBeforeSpeak)

	def close(self):
		pass
