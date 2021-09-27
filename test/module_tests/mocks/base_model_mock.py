from typing import Any

from gsf.core.entity.core import EntityProperties
from gsf.models.core import BaseModel


class BaseModelMock(BaseModel):
    def get_output(self) -> Any:
        raise NotImplementedError()

    def state_transition(self, *args, **kwargs):
        raise NotImplementedError()

    def get_properties(self) -> EntityProperties:
        raise NotImplementedError()
