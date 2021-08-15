from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from models.models.discrete_event_model import ModelInput

DynamicSystemInput = Dict[str, ModelInput]
