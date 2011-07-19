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

import locale
import logging
from drivers import list_drivers

logger = logging.getLogger(__name__)


_driver = None

def init():
    global _driver
    drivers = list_drivers()
    _driver = drivers[0]("generic")
    logger.info("Using driver %s", _driver.name)

def speak(message, cancel=True):
    global _driver
    if cancel:
        _driver.cancel()
    _driver.speak(message)

def cancel():
    _driver.cancel()

def set_voice_for_language(language=None, variant=None):
    if language is None:
        # read from the current local
        loc, encoding = locale.getdefaultlocale()
        language, variant = loc.split("_")
    voice = _driver.choose_for_language(language, variant)
    if voice is not None:
        _driver.set_language(language, variant)
        _driver.set_voice(voice[0])
        logger.info ("Found voice %s for locale %s", voice, loc)
        return voice[0]
    else:
        logger.info("Cannot find voice for locale %s, %s", language, variant)
    return False

def quit():
    if _driver:
        _driver.close()
        logger.info("Quitting speech")
