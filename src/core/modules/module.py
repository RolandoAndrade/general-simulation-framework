from __future__ import annotations

from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from core.modules.provider import Provider


class Module:
    providers: List[Provider]
    imports: List[Module]
    dependencies: List[Provider]
    exports: List[Provider]