"""Event Bus
=============================
This module contains the definition of the event bus and creates an static instance for event bus.

Example:
    Creating an event bus::

        event_bus = EventBus()

    Listening an event with decorator::

        event_bus = EventBus()

        @event_bus.on("Hello")
        def subscribed_event():
            print("World")

        event_bus.emit("Hello")

    Listening an event::

        event_bus = EventBus()

        def subscribed_event(number: int):
            for i in range(number):
                print('World')

        event_bus.on("Hello", subscribed_event)

        event_bus.emit("Hello", 3)
"""


from event_bus import EventBus as EB

EventBus = EB

static_event_bus = EventBus()
"""Static instance of event bus."""
