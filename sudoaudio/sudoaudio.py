import pygame
from pygame.locals import *
pygame.mixer.init()
import time

from gettext import gettext as _

import speech



class Board(object):

    def __init__(self, rows):
        self._original = [list(r) for r in rows]
        self._rows = [list(r) for r in rows]
        self._remaining = sum([1 for i in range(9) for j in range(9) if self._rows[i][j] == 0])

    def get(self, x, y):
        return self._rows[x][y]

    def put(self, x, y, value):
        if self._rows[x][y] == value:
            return True
        if self._original[x][y] != 0:
            print self._original[x][y]
            return False
        if value == 0:
            self._remaining += 1
            self._rows[x][y] = value
            return True
        else:
            ret = self._check_row(x,value) and self._check_col(y, value) and self._check_square(x,y,value)
        if ret:
            self._rows[x][y] = value
            self._remaining -= 1
        return ret

    def _check_row(self, x, value):
        for i in range(9):
            if self._rows[x][i] == value:
                return False
        return True

    def _check_col(self, y, value):
        for i in range(9):
            if self._rows[i][y] == value:
                return False
        return True

    def _check_square(self, x, y, value):
        basex = x - (x % 3)
        basey = y - (y % 3)
        # make this pythonic
        for i in range(basex, basex + 3):
            for j in range(basey, basey + 3):
                if self._rows[i][j] == value:
                    return False
        return True

    def is_solution(self):
        return self._remaining == 0

    @property
    def blanks(self):
        return self._remaining

    def dump(self, out):
        s = "\n".join([" ".join([str(x) for x in row]) for row in self._rows])
        out.write(s)


    @staticmethod
    def read_board(input):
        lines = input.readlines()
        if len(lines) != 9:
            raise Exception, "File as not 9 lines"
        rows = []
        for l in lines:
            cols = l.split()
            if len(cols) != 9:
                raise Exception, "Row as not 9 columns"
            rows.append([int(c) for c in cols])
        return Board(rows)


class Game(object):

    def __init__(self, filename):
        with open(filename) as f:
            self._board = Board.read_board(f)
        self._x = self._y = 0

    def quit(self, event):
        self._playing = False
        speech.speak(_("quitting"))

    def _dispatch_keydown(self, event):
        try:
            func = Game._key_handlers[event.key]
            func(self, event)
        except KeyError:
            pass

    def move(self, event):
        x, y = self._x, self._y
        if event.key == K_UP: x -= 1
        elif event.key == K_DOWN: x += 1
        elif event.key == K_LEFT: y -= 1
        elif event.key == K_RIGHT: y +=1
        if x < 0 or x > 8 or y < 0 or y > 8:
            pass # play invalid sound
        else:
            self._x, self._y = x, y
            self.speak_current()

    def put(self, event):
        value = event.key - K_0
        ret = self._board.put(self._x, self._y, value)
        if ret:
            self.speak_current()
            if self._board.is_solution():
                speech.speak(_("Solution found"))
        else:
            speech.speak(_("Impossible move"))

    def position(self, event):
        # report this from 1 to 9, people count from one...
        speech.speak("Row %d, column %d" % (self._x + 1, self._y + 1))

    def blanks(self, event):
        speech.speak("%d blanks" % self._board.blanks)

    def speak_current(self):
        val = self._board.get(self._x, self._y)
        speech.speak(str(val), stop=True)

    def run(self):
        speech.speak(_("Starting game"))
        time.sleep(1)
        self.speak_current()
        self._playing = True
        while self._playing:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    self._dispatch_keydown(event)
                elif event.type == QUIT:
                    _playing = False

    _key_handlers = {
    K_DOWN : move,
    K_UP : move,
    K_LEFT : move,
    K_RIGHT : move,
    K_p : position,
    K_b : blanks,
    K_q : quit,
    K_ESCAPE : quit
    }
    for i in range(K_0, K_9 + 1):
        _key_handlers[i] = put

def main(args):
    pygame.init()
    pygame.display.set_mode((640, 480))
    pygame.display.set_caption("sudoaudio")
    try:
        Game(args[0]).run()
    except:
        raise
    finally:
        pygame.quit()

if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
