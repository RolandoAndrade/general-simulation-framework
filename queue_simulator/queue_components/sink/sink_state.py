from __future__ import annotations

from typing import Dict, Any

from queue_simulator.queue_components.buffer.buffers import InputBuffer


class SinkState:
    INPUT_BUFFER = "InputBuffer"

    input_buffer: InputBuffer
    """Input buffer of the sink"""

    def __init__(self, input_buffer: InputBuffer):
        self.input_buffer = input_buffer

    def rename(self, new_name: str):
        self.input_buffer.set_id(new_name)

    def get_state_expressions(self) -> Dict[str, Any]:
        expressions = {}
        props = self.input_buffer.get_properties()
        for prop in props:
            expressions[prop] = {
                "value": self.input_buffer.get_id() + "." + prop,
                "call": props[prop].get_value
            }
        return {
            "InputBuffer": expressions
        }
