from typing import Set


class EntityManager:
    """Manager of entities."""

    _saved_names: Set[str]
    """List of entities saved."""

    def __init__(self):
        """Creates an entity manager."""
        self._saved_names = set()

    def name_already_exists(self, name: str):
        """Checks if the name is already in use."""
        return name in self._saved_names

    def replace_name(self, new_name: str, old_name: str = None):
        """Replaces the name with a new name."""
        if old_name and old_name in self._saved_names:
            self._saved_names.remove(old_name)
        self._saved_names.add(new_name)

    def remove(self, name: str):
        """Replaces the name with a new name."""
        self._saved_names.remove(name)


static_entity_manager = EntityManager()
"""Static entity manager."""
