from typing import Dict

from gsf.core.types.model_input import ModelInput
from gsf.models.core import BaseModel

DynamicSystemInput = Dict[BaseModel, ModelInput]
