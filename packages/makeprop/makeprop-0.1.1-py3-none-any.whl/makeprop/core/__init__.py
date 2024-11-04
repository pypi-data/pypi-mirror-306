import dataclasses
from typing import *

__all__ = ["makeprop"]


@dataclasses.dataclass
class makeprop:
    var: Optional[str] = None

    def __call__(self, func):
        if self.var is None:
            var = "_%s" % func.__name__
        else:
            var = self.var

        def fget(_self):
            return getattr(_self, var)

        def fset(_self, value):
            setattr(_self, var, func(_self, value))

        ans = property(fget=fget, fset=fset, doc=func.__doc__)
        return ans
