from typing import List, TYPE_CHECKING, Any, Sequence

if TYPE_CHECKING:
    from core.modules.component import Component


class Provider:
    _provide: type
    _inject: Sequence[Component]

    def __init__(self, provide: type, inject: Sequence[Component]):
        self._provide = provide
        self._inject = inject

    def instance(self) -> Any:
        return self._provide(self._inject)
