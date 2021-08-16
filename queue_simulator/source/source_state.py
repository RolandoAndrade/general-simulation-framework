from queue_simulator.buffer.buffers.output_buffer import OutputBuffer


class SourceState:
    OUTPUT_BUFFER = "OutputBuffer"

    output_buffer: OutputBuffer
    """Output buffer of the source"""

    def __init__(self, output_buffer: OutputBuffer):
        self.output_buffer = output_buffer
