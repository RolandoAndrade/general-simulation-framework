from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dynamic_system.network_models.network_model import NetworkModel

from dynamic_system.atomic_models.atomic_model import AtomicModel



class AtomicModelAdapter(AtomicModel):
    """Encapsulates a Network Model to make it appear as an Atomic Model"""
    _model: NetworkModel
    pass