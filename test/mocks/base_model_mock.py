from typing import Any

from core.entity.core import EntityProperties
from models.core.base_model import BaseModel


class BaseModelMock(BaseModel):
    def get_output(self) -> Any:
        pass

    def state_transition(self, *args, **kwargs):
        pass

    def get_properties(self) -> EntityProperties:
        pass
