import enum


class BufferPolicy(enum.Enum(str)):
    FIFO = "FIFO"
    LIFO = "LIFO"
    RANDOM = "RANDOM"
    ROUND_ROBIN = "ROUND_ROBIN"
