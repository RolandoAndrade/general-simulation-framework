from typing import Any

from gsf.core.entity.core import EntityProperties
from gsf.models.core import BaseModel


class BaseModelMock(BaseModel):
    def get_output(self) -> Any:
        pass

    def state_transition(self, *args, **kwargs):
        pass

    def get_properties(self) -> EntityProperties:
        pass
