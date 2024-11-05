"""
Module for AdES reporting data.

Defines enums for all AdES validation statuses defined in ETSI EN 319 102-1,
clause 5.1.3.
"""

import enum

__all__ = [
    'AdESStatus',
    'AdESSubIndic',
]

class AdESStatus(enum.Enum):
    PASSED = enum.auto()
    INDETERMINATE = enum.auto()
    FAILED = enum.auto()

class AdESSubIndic:
    @property
    def status(self) -> AdESStatus:
        raise NotImplementedError

    @property
    def standard_name(self):
        raise NotImplementedError
