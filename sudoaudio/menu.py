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

import core
import speech
import sounds
import utils

class ChoiceMenu(core.VoiceDialog):

    def __init__(self, title, options, selected_sound=None, changed_sound=None):
        self._title, self._options = title, options
        self._selected_sound, self._changed_sound = selected_sound, changed_sound
        self._index = 0

    def on_run(self):
        speech.speak(self._title)
        speech.speak(self._options[self._index], cancel=False)

    @core.key_event(pygame.K_UP)
    def up(self, event):
        self.changeSelection((self._index - 1) % len(self._options))

    @core.key_event(pygame.K_DOWN)
    def down(self, event):
        self.changeSelection((self._index + 1) % len(self._options))

    @core.key_event(pygame.K_RETURN)
    def enter(self, event):
        if self._selected_sound: self._selected_sound.play()
        self.quit(self._options[self._index])

    def speakSelected(self):
        speech.speak(self._options[self._index])

    def changeSelection(self, index):
        self._index = index
        if self._changed_sound:
            self._changed_sound.play()
        self.speakSelected()



class SoundSplash(core.PygameMainLoop):

    def __init__(self, soundname, allow_skeepping=True):
        self._allow_skeepping = allow_skeepping
        self._sound = sounds.SoundSource(soundname)
        self._sound.set_volume(1.0)

    def on_run(self):
        self._sound.play(post_end_event=True)

    def on_event_default(self, event):
        if event.type == sounds.end_sound_event:
            self.quit()
        elif event.type == pygame.KEYDOWN and self._allow_skeepping:
            self._sound.stop()
            self.quit()

