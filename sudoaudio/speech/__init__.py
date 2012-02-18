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
from accessible_output import speech

logger = logging.getLogger(__name__)


_speaker = None

def init():
    global _speaker
    if _speaker:
        return
    _speaker = speech.Speaker()



def speak(message, cancel=True):
    global _speaker
    assert _speaker, "Speech module not initialized"
    if cancel:
        _speaker.silence()
    _speaker.output(message)

def cancel():
    assert _speaker, "Speech module not initialized"
    _speaker.silence()

def quit():
    pass
