"""Type aliases.

.. warning::

    This module is provisional. Types may be modified, added, and removed between minor releases.
"""

import typing

StrSequenceOrSet = typing.Union[typing.Sequence[str], typing.AbstractSet[str]]
Validator = typing.Callable[[typing.Any], typing.Any]
