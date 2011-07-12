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

from drivers import list_drivers


_driver = None

def init():
    global _driver
    drivers = list_drivers()
    _driver = drivers[0]("generic")

def speak(message, cancel=True):
    global _driver
    if cancel:
        _driver.cancel()
    _driver.speak(message)

def cancel():
    _driver.cancel()


