from queue_simulator.buffer.buffers.input_buffer import InputBuffer
from queue_simulator.buffer.buffers.output_buffer import OutputBuffer
from queue_simulator.buffer.buffers.process_buffer import ProcessBuffer


class ServerState:
    OUTPUT_BUFFER = "OutputBuffer"
    INPUT_BUFFER = "InputBuffer"
    PROCESS_BUFFER = "ProcessBuffer"

    outputBuffer: OutputBuffer
    """Output buffer of the server"""

    inputBuffer: InputBuffer
    """Input buffer of the server"""

    processBuffer: ProcessBuffer
    """Processing buffer of the server"""

    def __init__(self,
                 inputBuffer: InputBuffer,
                 outputBuffer: OutputBuffer,
                 processBuffer: ProcessBuffer):
        self.outputBuffer = outputBuffer
        self.inputBuffer = inputBuffer
        self.processBuffer = processBuffer
