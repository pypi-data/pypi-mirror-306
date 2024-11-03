import functools
from typing import *

__all__ = [
    "classdecorator",
    "getdecorator",
    "getproperty",
]


def classdecorator(cls: Any, /, **kwargs: Any) -> Any:
    """Add keyaliases to cls."""
    for alias, key in kwargs.items():
        pro = getproperty(key)
        setattr(cls, alias, pro)
    return cls


def getdecorator(**kwargs: Any) -> functools.partial:
    """Get a keyalias decorator for a class."""
    return functools.partial(classdecorator, **kwargs)


def getproperty(key: Any) -> property:
    """Get a keyalias property."""

    def fget(self, /):
        return self[key]

    def fset(self, value, /):
        self[key] = value

    def fdel(self, /):
        del self[key]

    doc = "self[%r]" % key
    ans = property(fget, fset, fdel, doc)
    return ans
