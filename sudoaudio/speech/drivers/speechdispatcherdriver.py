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
        self._synth_voice = None

    def speak(self, message):
        logger.debug("Speaking %s", message)
        self._client.speak(message)

    def cancel(self):
        logger.debug("Cancelling speech")
        self._client.cancel()

    def close(self):
        self._client.close()

    def list_voices(self):
        l = self._client.list_synthesis_voices()
        logger.debug("Found voices: %s", l)
        return l

    def set_language(self, language, variant=None):
        self._client.set_language(language)

    def set_voice(self, voice):
        logger.debug("Setting voice %s", voice)
        self._client.set_synthesis_voice(voice)
        self._synth_voice = voice

    def get_voice(self):
        return self._synth_voice

    def __del__(self):
        if self._client:
            self._client.close()
            self._client = None
