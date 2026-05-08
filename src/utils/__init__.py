"""Utils - pure helper functions with no domain logic."""

from typing import TypeVar

T = TypeVar("T")


def clamp(value: int, min_val: int, max_val: int) -> int:
    """Clamp a value to be within [min_val, max_val]."""
    return max(min_val, min(value, max_val))
