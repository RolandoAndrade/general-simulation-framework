import enum


class BufferProperty(str, enum.Enum):
    CAPACITY = "Capacity"
    POLICY = "Policy"
    NUMBER_ENTERED = "NumberEntered"
