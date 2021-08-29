import enum


class NodeType(str, enum.Enum):
    SOURCE = "SOURCE"
    SERVER = "SERVER"
    ENTITY_EMITTER = "ENTITY_EMITTER"
    SINK = "SINK"
