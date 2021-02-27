from __future__ import annotations
from typing import Type, Callable

from pyeventbus3.pyeventbus3 import Mode, PyBus

from core.events.event import Event


class ThreadMode(Mode):
    pass


def subscriber(sub: object):
    def wrapped():
        PyBus.Instance().register(sub, sub.__class__.__name__)

    return wrapped


def subscribe(on_event: Type[Event], thread_mode: ThreadMode = ThreadMode.POSTING):
    bus = PyBus.Instance()

    def real_decorator(function):
        bus.addEventsWithMethods(on_event, function, thread_mode)

        def wrapper(*args, **kwargs):
            return function(*args, **kwargs)

        return wrapper

    return real_decorator


class EventBus:
    def register(self, sub: object):
        PyBus.Instance().register(sub, sub.__class__.__name__)

    def emit(self, event: Event):
        PyBus.Instance().post(event)

    def on(self, on_event: Type[Event], function: Callable, thread_mode: ThreadMode = ThreadMode.POSTING):
        PyBus.Instance().addEventsWithMethods(on_event, function, thread_mode)


event_bus = EventBus()
