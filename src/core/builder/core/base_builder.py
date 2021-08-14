from __future__ import annotations

from dynamic_system.core.base_dynamic_sytem import BaseDynamicSystem
from simulation.core.base_simulator import BaseSimulator


class BaseBuilder:
    """Simulation builder"""

    _dynamicSystem: BaseDynamicSystem
    """Dynamic system where things will be built"""

    _simulator: BaseSimulator
    """Dynamic system where things will be built"""
