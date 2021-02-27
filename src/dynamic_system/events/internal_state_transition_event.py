from core.events.event import Event


class InternalStateTransitionEvent(Event):
    def __init__(self):
        self._subject = "INTERNAL_STATE_TRANSITION_EVENT"
        self._message = ""