import logging

import _base

logger = logging.getLogger(__name__)

try:
    import speechd
    logger.debug("speechd package present in system")
except ImportError:
    logger.debug("Speechd package not present")
    raise _base.DriverNotSupportedException


class Driver(_base.BaseDriver):
    name = "Speech-dispatcher"

    def __init__(self, name, *args, **kwargs):
        super(_base.BaseDriver, self).__init__()
        self._client = speechd.SSIPClient(name)
        logger.debug("Connected to speech-dispatcher")

    def speak(self, message):
        logger.debug("Speaking %s", message)
        self._client.speak(message)

    def cancel(self):
        logger.debug("Cancelling speech")
        self._client.cancel()

    def __del__(self):
        try:
            self._client.close()
        except:
            pass
