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

import core
import speech
import paths
import sounds
from menu import ChoiceMenu, SoundSplash

import utils

import gettext
gettext.bindtextdomain("sudoaudio", paths.localedir)
gettext.textdomain("sudoaudio")

from gettext import gettext as _

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
            return False
        if value == 0:
            self._remaining += 1
            self._rows[x][y] = value
            return True
        else:
            ret = value in self.possibilities(x ,y)
        if ret:
            if self._rows[x][y] == 0:
                self._remaining -= 1
            self._rows[x][y] = value
        return ret

    def is_solution(self):
        return self._remaining < 0

    def possibilities(self, x, y):
        if self._original[x][y] != 0:
            return [self._original[x][y]]
        else:
            possibilities = set(range(1,10))
            # Subtract current row, column, and square values
            possibilities.difference_update(set(self.row_values(x)),
                set(self.column_values(y)),
                set(self.square_values(x,y)))
            if self._rows[x][y] != 0:
                possibilities.add(self._rows[x][y])
            return list(possibilities)

    def row_values(self,i):
        return list(self._rows[i])

    def column_values(self, j):
        return [self._rows[i][j] for i in range(9)]

    def square_values(self, x, y):
        basex = x - (x % 3)
        basey = y - (y % 3)
        return [self._rows[x][y] for x, y in itertools.product(range(basex, basex + 3), range(basey, basey + 3))]

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


class Game(core.PygameMainLoop):

    def __init__(self, filename):
        with open(filename) as f:
            self._board = Board.read_board(f)
        self._x = self._y = 0
        self._move_sound = sounds.SoundSource(os.path.join(paths.sounds_path, "move.ogg"))
        self._wrong_sound = sounds.SoundSource(os.path.join(paths.sounds_path, "wrong.ogg"))
        self._win_sound = sounds.SoundSource(os.path.join(paths.sounds_path, "win.ogg"))

    def on_run(self):
        speech.speak(_("You are in the top left corner of the Puzzle. Press the h key for help with the game."))
    @core.key_event(K_q)
    def quit_game(self, event):
        speech.speak(_("quitting"))
        self.quit(None)

    @core.key_event(K_h)
    def help(self, event):
        help_string = _("""
        To move around the board use the arrow keys.
        To put a number on a square use numbers from 1 to 9.
        To clear a square use the 0 key. A square can only be cleared if it was blank on the original puzzle.
        To speak the current square position on the board use the p key.
        To know how many squares are still blank press b.
        To speak what possibilities exist for the current square press s.
        To quit the game press the q key.
        """)
        speech.speak(help_string)

    @core.key_event(K_UP, K_DOWN, K_LEFT, K_RIGHT)
    def move(self, event):
        x, y = self._x, self._y
        if event.key == K_UP: x -= 1
        elif event.key == K_DOWN: x += 1
        elif event.key == K_LEFT: y -= 1
        elif event.key == K_RIGHT: y +=1
        if x < 0 or x > 8 or y < 0 or y > 8:
            self._wrong_sound.play()
        else:
            self._x, self._y = x, y
            self.speak_current()

    @core.key_event(*range(K_0, K_9 +1))
    def put(self, event):
        value = event.key - K_0
        ret = self._board.put(self._x, self._y, value)
        if ret:
            self._move_sound.play()
            self.speak_current()
            if self._board.is_solution():
                self._win_sound.play()
                speech.speak(_("Solution found"))
        else:
            speech.speak(_("Impossible move"))

    @core.key_event(K_p)
    def position(self, event):
        # report this from 1 to 9, people count from one...
        speech.speak(_("Row %d, column %d") % (self._x + 1, self._y + 1))

    @core.key_event(K_b)
    def blanks(self, event):
        speech.speak("%d blanks" % self._board.blanks)

    @core.key_event(K_s)
    def possibilities(self, event):
        l = self._board.possibilities(self._x, self._y)
        if l:
            message = " ".join(map(str, l))
            speech.speak(message)
        else:
            speech.speak(_("Nothing"))

    def speak_current(self):
        val = self._board.get(self._x, self._y)
        message = str(val) if val > 0 else _("Blank")
        speech.speak(message)

    def on_runn(self):
        speech.speak(_("Starting game"))
        time.sleep(1)
        self.speak_current()

def list_puzzles(path):
    import glob
    return sorted([f for f in os.listdir(path) if f.endswith(".sudo")])

def _set_logging(opts):
    try:
        level = os.environ['SUDOAUDIO_LOGLEVEL']
    except KeyError:
        return
    level = getattr(logging, level, None)
    if level:
        logging.basicConfig(level=level)

_set_logging(None)

def main():
    args = sys.argv[1:]
    try:
        utils.adjust_pythonpath()
        speech.init()
        speech.set_voice_for_language()
        pygame.init()
        pygame.display.set_mode((640, 480))
        pygame.display.set_caption("sudoaudio")
        s = SoundSplash(os.path.join(paths.sounds_path, "intro.ogg"))
        s.run()
        if len(args) < 1:
            dir = os.path.join(os.path.dirname(__file__), "puzzles", "pack1")
            basename = ChoiceMenu(_("Select puzzle"), list_puzzles(dir)).run()
            if basename is None:
                sys.exit(-1)
            file = os.path.join(dir, basename)
        else:
            file = args[0]
        Game(file).run()
    except:
        raise
    finally:
        pygame.quit()
        speech.quit()


if __name__ == '__main__':
    main()
