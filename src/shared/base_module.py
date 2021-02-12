from typing import List


class BaseModule:
    def __init__(self):
        pass

    def list_of_methods(self) -> List[str]:
        metadata = dir(self)
        index = metadata.index("list_of_methods")
        return metadata[index:]
