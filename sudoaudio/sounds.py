import pygame.mixer

import utils

end_sound_event = utils.get_new_event_id()



class SoundSource(object):

    def __init__(self, source):
        self._sound = pygame.mixer.Sound(source)
        self._channel = None

    def play(self, loop=0, post_end_event=False):
        self._channel = self._sound.play(loop)
        self._channel.set_endevent(end_sound_event)

    def stop(self):
        if self._channel:
            self._channel.stop()


    def set_volume(self, volume):
        self._sound.set_volume(volume)
