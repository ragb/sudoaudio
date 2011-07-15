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

import itertools
import logging
import os.path
import optparse
import sys
import time

import pygame
from pygame.locals import *
pygame.mixer.init()

from gettext import gettext as _

import speech
from menu import ChoiceMenu

logger = logging.getLogger(__name__)


class Board(object):

    def __init__(self, rows):
        self._original = [list(r) for r in rows]
        self._rows = [list(r) for r in rows]
        self._remaining = sum([1 for i, j in itertools.product(range(9), repeat=2) if self._rows[i][j] == 0])

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
            if self._rows[x][y] == 0:
                self._remaining -= 1
            self._rows[x][y] = value
        return ret

    def _check_row(self, x, value):
        return not any([self._rows[x][i] == value for i in range(9)])

    def _check_col(self, y, value):
        return not any([self._rows[j][y] == value for j in range(9)])

    def _check_square(self, x, y, value):
        basex = x - (x % 3)
        basey = y - (y % 3)
        indexes = [(x, y) for x, y in itertools.product(range(basex, 3), range(basey, 3))]
        return not any([self._rows[i][j] == value for i, j in indexes])


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
        message = str(val) if val > 0 else _("Blank")
        speech.speak(message)

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

def list_puzzles(path):
    import glob
    return sorted([f for f in os.listdir(path) if f.endswith(".sudo")])

def _set_logging(opts):
    level = os.environ['SUDOAUDIO_LOGLEVEL']
    level = getattr(logging, level, None)
    if level:
        logging.basicConfig(level=level)

def main(args):
    speech.init()
    try:
        pygame.init()
        pygame.display.set_mode((640, 480))
        pygame.display.set_caption("sudoaudio")
        if len(args) < 1:
            dir = os.path.join(os.path.dirname(__file__), "..", "puzzles", "pack1")
            basename = ChoiceMenu(_("Select puzzle"), list_puzzles(dir)).run()
            file = os.path.join(dir, basename)
            if basename is None:
                sys.exit(-1)
        else:
            file = args[0]
        Game(file).run()
    except:
        raise
    finally:
        pygame.quit()
        speech.quit()


if __name__ == '__main__':
    main(sys.argv[1:])
