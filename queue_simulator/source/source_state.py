from queue_simulator.buffer.buffers.output_buffer import OutputBuffer


class SourceState:
    OUTPUT_BUFFER = "OutputBuffer"

    outputBuffer: OutputBuffer
    """Output buffer of the source"""

    def __init__(self, outputBuffer: OutputBuffer):
        self.outputBuffer = outputBuffer
