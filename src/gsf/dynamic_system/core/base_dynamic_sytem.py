from __future__ import annotations

from abc import abstractmethod

from gsf.core.debug.domain.debug import debug

from typing import Any, TYPE_CHECKING, Dict, Set

from graphviz import Digraph

from gsf.core.events import EventBus, static_event_bus

if TYPE_CHECKING:
    from gsf.models.core import Path, BaseModel

    DynamicSystemOutput = Dict[BaseModel, Any]
    DynamicSystemModels = Set[BaseModel]
    DynamicSystemPaths = Dict[BaseModel, Set[Path]]


class BaseDynamicSystem:
    """Abstract dynamic system"""

    _models: DynamicSystemModels
    """Models of the dynamic system"""

    _paths: DynamicSystemPaths
    """Paths of the dynamic system. Dict[Origin, Set[Output]]"""

    _event_bus: EventBus
    """Event bus of the module."""

    @debug("Started the dynamic system", after=True)
    def __init__(self, event_bus: EventBus = None):
        """Creates a dynamic system"""

        self._models = set()
        self._paths = {}
        self._event_bus = event_bus or static_event_bus

    @debug("Adding model to the dynamic system")
    def add(self, model: BaseModel):
        """Adds a model to the dynamic system.

        Args:
            model (BaseModel): Model to be added.
        """
        if model.get_dynamic_system() != self:
            raise Exception("Invalid dynamic system")
        self._models.add(model)

    @debug("Adding path to the dynamic system")
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

    @debug("Deleting path from the dynamic system")
    def unlink(self, path: Path):
        """Removes a path between two nodes.

        Args:
            path (Path): Path to be deleted.
        """
        origin = path.get_source_model()
        if origin in self._paths:
            if path in self._paths[origin]:
                self._paths[origin].remove(path)
                if len(self._paths[origin]) == 0:
                    self._paths.pop(origin, 1)

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
                        new_paths.append(p)
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

    def show(self, file_name: str = "dynamic_system"):
        """Shows a graph of the dynamic system"""
        dg = Digraph()
        for model in self._models:
            dg.node(model.get_id(), model.get_id())
        for path in self._paths:
            for p in self._paths[path]:
                dg.edge(
                    path.get_id(),
                    p.get_destination_model().get_id(),
                    label=p.get_id() + "(" + str(p.get_weight()) + ")",
                )

        dg.render(file_name, view=True, format="png")
        return dg
