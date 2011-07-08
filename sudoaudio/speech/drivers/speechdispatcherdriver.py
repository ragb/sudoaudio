import _base

try:
    import speechd
except ImportError:
    raise _base.DriverNotSupportedException


class Driver(_base.BaseDriver):
    name = "Speech-dispatcher"

    def __init__(self, name, *args, **kwargs):
        super(_base.BaseDriver, self).__init__()
        self._client = speechd.SSIPClient(name)

    def speak(self, message):
        self._client.speak(message)

    def cancel(self):
        self._client.cancel()

    def __del__(self):
        try:
            self._client.close()
        except:
            pass
