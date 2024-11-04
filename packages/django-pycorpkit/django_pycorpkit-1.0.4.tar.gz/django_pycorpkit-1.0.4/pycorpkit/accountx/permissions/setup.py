from collections import namedtuple
from functools import partial

PERM_NODE = namedtuple(
    "PERM_NODE",
    [
        "name",
        "description",
        "is_deprecated",
        "is_system_level",
        "children",
    ],
)

PERM_NODE.__new__ = partial(
    PERM_NODE.__new__,
    is_deprecated=False,
    is_system_level=False,
    children=(),
)
