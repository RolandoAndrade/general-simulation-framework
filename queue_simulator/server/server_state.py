from typing import Union

from core.entity import NumberProperty
from queue_simulator.buffer.buffers.input_buffer import InputBuffer
from queue_simulator.buffer.buffers.output_buffer import OutputBuffer
from queue_simulator.buffer.buffers.process_buffer import ProcessBuffer


class ServerState:
    OUTPUT_BUFFER = "OutputBuffer"
    INPUT_BUFFER = "InputBuffer"
    PROCESS_BUFFER = "ProcessBuffer"
    PROCESSING_REMAINING_TIME = "ProcessingRemainingTime"

    outputBuffer: OutputBuffer
    """Output buffer of the server"""

    inputBuffer: InputBuffer
    """Input buffer of the server"""

    processBuffer: ProcessBuffer
    """Processing buffer of the server"""

    _processingRemainingTime: NumberProperty
    """Remaining time to finish the processing"""

    def __init__(self,
                 inputBuffer: InputBuffer,
                 outputBuffer: OutputBuffer,
                 processBuffer: ProcessBuffer):
        self.outputBuffer = outputBuffer
        self.inputBuffer = inputBuffer
        self.processBuffer = processBuffer
        self.processingRemainingTime = NumberProperty(0)

    @property
    def processingRemainingTime(self) -> NumberProperty:
        """Remaining time to finish the processing"""
        return self._processingRemainingTime

    @processingRemainingTime.setter
    def processingRemainingTime(self, value: Union[NumberProperty, float]):
        """Remaining time to finish the processing"""
        if isinstance(value, NumberProperty):
            self._processingRemainingTime = value
        else:
            self._processingRemainingTime = NumberProperty(value)
