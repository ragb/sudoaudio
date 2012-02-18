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

import os
import sys

import pygame


_free_event_id = pygame.locals.USEREVENT
def get_new_event_id():
    global _free_event_id
    if _free_event_id >= pygame.locals.NUMEVENTS:
        raise Exception, "no more event ids"
    ret = _free_event_id
    _free_event_id += 1
    return ret

