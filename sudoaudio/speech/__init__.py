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


