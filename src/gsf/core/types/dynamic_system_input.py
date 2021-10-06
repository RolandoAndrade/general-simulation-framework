"""Dynamic System Input module
===============================
This module contains the definitions of types and aliases used in the framework.
"""

from typing import Dict

from gsf.core.types.model_input import ModelInput
from gsf.models.core import BaseModel

DynamicSystemInput = Dict[BaseModel, ModelInput]
"""Alias for dynamic system inputs"""
