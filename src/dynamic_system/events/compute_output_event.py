from core.events.event import Event


class ComputeOutputEvent(Event):
    def __init__(self):
        self._subject = "COMPUTE_OUTPUT_EVENT"
        self._message = ""
