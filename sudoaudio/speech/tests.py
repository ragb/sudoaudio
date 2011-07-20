import unittest
from . import *
from drivers import list_drivers


class SpeechTest(unittest.TestCase):

    def setUp(self):
        init()

    def tearDown(self):
        quit()

    def test_drivers(self):
        self.assertTrue(len(list_drivers()) > 0)

    def test_speak(self):
        speak("testing")

    def test_cancel(self):
        speak("testing")
        cancel()

    def test_list_voices(self):
        d = get_current_driver()
        voices = d.list_voices()
        for v in voices:
            d.set_voice(v[0])
            self.assertEquals(v[0], d.get_voice())

