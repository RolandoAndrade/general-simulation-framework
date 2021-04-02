from __future__ import annotations

from typing import List, TYPE_CHECKING, Any

if TYPE_CHECKING:
    from core.modules.component import Component


class Provider:
    _provide: type
    _inject: List[Any]

    def __init__(self, provide: type, inject: List[Component]):
        self._provide = provide
        self._inject = inject

    def instance(self) -> Any:
        return self._provide(*self._inject)
