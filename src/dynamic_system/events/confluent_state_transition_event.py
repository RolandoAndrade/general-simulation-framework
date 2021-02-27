from core.events.event import Event


class ConfluentStateTransitionEvent(Event):
    def __init__(self):
        self._subject = "EXTERNAL_STATE_TRANSITION_EVENT"
        self._message = ""
