from typing import Dict

from core.types.model_input import ModelInput
from models.core import BaseModel

DynamicSystemInput = Dict[BaseModel, ModelInput]
