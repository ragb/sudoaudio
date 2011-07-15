import pygame


_free_event_id = pygame.locals.USEREVENT
def get_new_event_id():
    global _free_event_id
    if _free_event_id >= pygame.locals.NUMEVENTS:
        raise Exception, "no more event ids"
    ret = _free_event_id
    _free_event_id += 1
    return ret
