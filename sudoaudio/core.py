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

import functools
import inspect
import sys

import pygame

def key_event(*keys):
    def wrap(f):
        f.__key_events__ = keys
        return f
    return wrap


class _KeyHandlerMeta(type):

    def __new__(cls, name, bases, dct):
        if not '__key_handlers__' in dct:
            dct['__key_handlers__'] = {}
        for v in dct.values():
            if hasattr(v, '__key_events__') and callable(v):
                for e in v.__key_events__:
                    dct['__key_handlers__'][e] = v
        return type.__new__(cls, name, bases, dct)


class PygameMainLoop(object):
    __metaclass__ = _KeyHandlerMeta
    def __init__(self):
        self._mainloop_running = False
        self._retval = None

    def run(self):
        self.on_run()
        self._mainloop_running = True
        while self._mainloop_running:
            self.run_before()
            for event in self.get_events():
                self.dispatch_event(event)
            self.run_after()
        return self._retval

    def quit(self, retval=None):
        self._retval = retval
        self._mainloop_running = False

    def dispatch_event(self, event):
        if event.type == pygame.QUIT:
            self.on_quit_event()
        elif event.type == pygame.KEYDOWN:
            if event.key in self.__key_handlers__:
                self.__key_handlers__[event.key](self,event)

    def on_quit_event(self):
        sys.exit(0)

    def get_events(self):
        return pygame.event.get()

    def run_before(self):
        pass

    def run_after(self):
        pass

    def on_run(self):
        pass

class VoiceDialog(PygameMainLoop):

    @key_event(pygame.K_ESCAPE)
    def escape(self, event):
        self.quit(None)

