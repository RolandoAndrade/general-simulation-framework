import enum


class AvailableEntities(str, enum.Enum):
    SOURCE = "SOURCE"
    SERVER = "SERVER"
    ENTITY_EMITTER = "EMITTER"
    SINK = "SINK"
    PATH = "PATH"
    ENTITY = "ENTITY"
