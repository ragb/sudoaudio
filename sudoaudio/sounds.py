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


import pygame.mixer

import utils

end_sound_event = utils.get_new_event_id()



class SoundSource(object):

    def __init__(self, source):
        self._sound = pygame.mixer.Sound(source)
        self._channel = None

    def play(self, loop=0, post_end_event=False):
        self._channel = self._sound.play(loop)
        if post_end_event:
            self._channel.set_endevent(end_sound_event)

    def stop(self):
        if self._channel:
            self._channel.stop()


    def set_volume(self, volume):
        self._sound.set_volume(volume)
