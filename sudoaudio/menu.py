import pygame
import speech
import sounds
import utils

class ChoiceMenu(object):

    def __init__(self, title, options):
        self._title, self._options = title, options
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
                    elif event.key == pygame.K_RETURN: return self._options[self._index]

    def speakSelected(self):
        speech.speak(self._options[self._index])

    def changeSelection(self, index):
        self._index = index
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
                elif event.type == pygame.KEYDOWN and allow_skeepping:
                    running = False

