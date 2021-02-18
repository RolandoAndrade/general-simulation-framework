from __future__ import annotations

from typing import TYPE_CHECKING, List, Dict

from core.modules.module_metadata import ModuleMetadata

if TYPE_CHECKING:
    from core.modules.provider import Provider


class Module:
    module_metadata: ModuleMetadata
    providers: List[type]
    exports: List[type]
    imports: List[Module]
    dependencies: List[Provider]
    instances: List[Provider]

    def _find_dependency(self, dependency: type) -> Provider:
        for dep in self.dependencies:
            if type(dep) == dependency:
                return dep
        raise Exception("Missing dependency " + str(dependency))

    def get_exported_dependencies(self) -> List[Provider]:
        dependencies: List[Provider] = []
        for provider in self.instances:
            if type(provider) in self.exports:
                dependencies.append(provider)
        return dependencies

    def _inject_dependencies(self):
        pass
