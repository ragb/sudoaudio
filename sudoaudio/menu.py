import pygame
import speech


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


def test():
    pygame.init()
    pygame.display.init()
    pygame.display.set_mode((640,480), 0, 8)
    m = Menu("meu menu", ['rui', 'batista', 'sair'])
    print m.run()
    pygame.quit()

if __name__ == '__main__':
    test()
