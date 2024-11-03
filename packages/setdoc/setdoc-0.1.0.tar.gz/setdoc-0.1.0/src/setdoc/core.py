import dataclasses
from typing import *

__all__ = ["setdoc"]


@dataclasses.dataclass
class setdoc:
    doc: Any

    def __call__(self, target: Any) -> Any:
        target.__doc__ = self.doc
        return target
