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


COM_CLASS = "SAPI.SPVoice"


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
		self.tts.speak(message, 0)

	def cancel(self):
		self.tts.Speak(None, 1|constants.SVSFPurgeBeforeSpeak)