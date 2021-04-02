from __future__ import annotations

from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from core.modules.module import Module
    from core.modules.provider import Provider


class ModuleMetadata:
    _imports: List[Module]
    _exports: List[type]
    _dependencies: List[Provider]
    _components: List[Provider]

    def imports(self, modules: List[Module]) -> ModuleMetadata:
        self._imports = modules
        return self

    def exports(self, components: List[type]) -> ModuleMetadata:
        self._exports = components
        return self

    def components(self, components: List[Provider]) -> ModuleMetadata:
        self._components = components
        return self

    def dependencies(self, components: List[Provider]) -> ModuleMetadata:
        self._dependencies = components
        return self

    def get_exports(self) -> List[type]:
        return self._exports
