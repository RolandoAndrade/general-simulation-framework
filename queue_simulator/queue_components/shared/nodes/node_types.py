import enum


class NodeType(str, enum.Enum):
    SOURCE = "SOURCE"
    SERVER = "SERVER"
    ENTITY_EMITTER = "EMITTER"
    SINK = "SINK"
