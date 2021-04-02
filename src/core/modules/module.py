from __future__ import annotations

from typing import TYPE_CHECKING, List

from core.modules.module_metadata import ModuleMetadata

if TYPE_CHECKING:
    from core.modules.component import Component


class Module:
    _module_metadata: ModuleMetadata
    _instances: List[Component]

    def __init__(self, module_metadata: ModuleMetadata):
        pass

    def get_exported_dependencies(self) -> List[Component]:
        dependencies: List[Component] = []
        for instance in self._instances:
            if type(instance) in self._module_metadata.get_exports():
                dependencies.append(instance)
        return dependencies
