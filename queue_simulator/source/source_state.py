from __future__ import annotations
from typing import Dict, Any

from queue_simulator.buffer.buffers.output_buffer import OutputBuffer


class SourceState:
    OUTPUT_BUFFER = "OutputBuffer"

    output_buffer: OutputBuffer
    """Output buffer of the source"""

    def __init__(self, output_buffer: OutputBuffer):
        self.output_buffer = output_buffer

    def rename(self, new_name: str):
        self.output_buffer.set_id(new_name)

    def get_state_expressions(self) -> Dict[str, Any]:
        expressions = {}
        props = self.output_buffer.get_properties()
        for prop in props:
            expressions[prop] = {
                "value": self.output_buffer.get_id() + "." + prop,
                "call": props[prop].get_value
            }
        return {
            "OutputBuffer": expressions
        }
