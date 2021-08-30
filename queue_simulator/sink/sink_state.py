from queue_simulator.buffer.buffers import InputBuffer


class SinkState:
    INPUT_BUFFER = "InputBuffer"

    input_buffer: InputBuffer
    """Input buffer of the sink"""

    def __init__(self, input_buffer: InputBuffer):
        self.input_buffer = input_buffer

    def rename(self, new_name: str):
        self.input_buffer.set_id(new_name)
