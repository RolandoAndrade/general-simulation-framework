from decimal import Decimal
from typing import Union

from core.entity.properties import NumberProperty
from queue_simulator.buffer.buffers.input_buffer import InputBuffer
from queue_simulator.buffer.buffers.output_buffer import OutputBuffer
from queue_simulator.buffer.buffers.process_buffer import ProcessBuffer


class ServerState:
    OUTPUT_BUFFER = "OutputBuffer"
    INPUT_BUFFER = "InputBuffer"
    PROCESS_BUFFER = "ProcessBuffer"
    PROCESSING_REMAINING_TIME = "ProcessingRemainingTime"

    output_buffer: OutputBuffer
    """Output buffer of the server"""

    input_buffer: InputBuffer
    """Input buffer of the server"""

    process_buffer: ProcessBuffer
    """Processing buffer of the server"""

    _processing_remaining_time: NumberProperty
    """Remaining time to finish the processing"""

    def __init__(self,
                 input_buffer: InputBuffer,
                 output_buffer: OutputBuffer,
                 process_buffer: ProcessBuffer):
        self.output_buffer = output_buffer
        self.input_buffer = input_buffer
        self.process_buffer = process_buffer
        self.processing_remaining_time = NumberProperty(0)

    @property
    def processing_remaining_time(self) -> NumberProperty:
        """Remaining time to finish the processing"""
        return self._processing_remaining_time

    @processing_remaining_time.setter
    def processing_remaining_time(self, value: Union[NumberProperty, Decimal]):
        """Remaining time to finish the processing"""
        if isinstance(value, NumberProperty):
            self._processing_remaining_time = value
        else:
            self._processing_remaining_time = NumberProperty(value)

    def rename(self, new_name: str):
        self.output_buffer.set_id(new_name)
        self.input_buffer.set_id(new_name)
        self.process_buffer.set_id(new_name)
