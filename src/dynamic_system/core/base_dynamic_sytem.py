from __future__ import annotations

from abc import abstractmethod

from core.debug.domain.debug import debug

from typing import Any, TYPE_CHECKING, Dict, Set

if TYPE_CHECKING:
    from models.core import Path, BaseModel

    DynamicSystemOutput = Dict[BaseModel, Any]
    DynamicSystemModels = Set[BaseModel]
    DynamicSystemPaths = Dict[BaseModel, Set[Path]]


class BaseDynamicSystem:
    """Abstract dynamic system"""

    _models: DynamicSystemModels
    """Models of the dynamic system"""

    _paths: DynamicSystemPaths
    """Paths of the dynamic system. Dict[Origin, Set[Output]]"""

    @debug("Started the dynamic system", after=True)
    def __init__(self):
        """Creates a dynamic system"""
        self._models = set()
        self._paths = {}

    @debug("Adding model to the dynamic system")
    def add(self, model: BaseModel):
        """Adds a model to the dynamic system.

        Args:
            model (BaseModel): Model to be added.
        """
        if model.get_dynamic_system() != self:
            raise Exception("Invalid dynamic system")
        self._models.add(model)

    @debug("Adding model to the dynamic system")
    def link(self, path: Path) -> BaseModel:
        """Adds a path between two nodes.

        Args:
            path (Path): Path to be appended.
        """
        origin = path.get_source_model()
        if origin in self._paths:
            self._paths[origin].add(path)
        else:
            self._paths[origin] = {path}
        return origin

    @debug("Removing model of the dynamic system")
    def remove(self, model: BaseModel):
        """Removes a model of the dynamic system.

        Args:
            model (BaseModel): Model to be removed.
        """
        if model in self._models:
            self._models.remove(model)
            self._paths.pop(model, 1)
            for path in self._paths:
                new_paths = []
                for p in self._paths[path]:
                    if p != model:
                        new_paths = new_paths.append(p)
                self._paths[path] = set(new_paths)
        else:
            raise Exception("Model not found")

    @abstractmethod
    def get_output(self) -> DynamicSystemOutput:
        """Gets the output of the dynamic system."""
        raise NotImplementedError

    @abstractmethod
    def state_transition(self, *args, **kwargs) -> DynamicSystemOutput:
        """Executes the state transition of the dynamic system.

        Args:
            *args:
            **kwargs:
        """
        raise NotImplementedError
