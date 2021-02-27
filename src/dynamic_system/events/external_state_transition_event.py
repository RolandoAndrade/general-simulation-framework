from core.events.event import Event


class ExternalStateTransitionEvent(Event):
    def __init__(self, time: float):
        self._subject = "EXTERNAL_STATE_TRANSITION_EVENT"
        self._message = {
            time: time
        }

    def get_time(self) -> float:
        return self._message.time
