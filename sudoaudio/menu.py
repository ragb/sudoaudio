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


import pygame
import speech
import sounds
import utils

class ChoiceMenu(object):

    def __init__(self, title, options, selected_sound=None, changed_sound=None):
        self._title, self._options = title, options
        self._selected_sound, self._changed_sound = selected_sound, changed_sound
        self._index = 0

    def run(self):
        speech.speak(self._title)
        speech.speak(self._options[self._index], cancel=False)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP: self.changeSelection((self._index - 1) % len(self._options))
                    elif event.key == pygame.K_DOWN: self.changeSelection((self._index + 1) % len(self._options))
                    elif event.key == pygame.K_ESCAPE: return None
                    elif event.key == pygame.K_RETURN:
                        if self._selected_sound: self._selected_sound.play()
                        return self._options[self._index]

    def speakSelected(self):
        speech.speak(self._options[self._index])

    def changeSelection(self, index):
        self._index = index
        if self._changed_sound:
            self._changed_sound.play()
        self.speakSelected()



class SoundSplash(object):

    def __init__(self, soundname, allow_skeepping=True):
        self._allow_skeepping = allow_skeepping
        self._sound = sounds.SoundSource(soundname)
        self._sound.set_volume(1.0)

    def run(self):
        self._sound.play(post_end_event=True)
        running = True
        while running :
            for event in pygame.event.get():
                if event.type == sounds.end_sound_event:
                    running = False
                elif event.type == pygame.KEYDOWN and self._allow_skeepping:
                    self._sound.stop()
                    running = False

