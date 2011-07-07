import speechd

_ssipclient = speechd.SSIPClient("audiopong")

def speak(message, stop=True):
    if stop:
        _ssipclient.stop()
    _ssipclient.speak(message)

def stop():
    _ssipclient.stop()
