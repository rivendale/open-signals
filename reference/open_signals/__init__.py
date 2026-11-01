"""Reference implementation of the open-signals machine-readable spec (MIT).

Educational material only. It computes the arithmetic of the rules in docs/;
it is not investment, tax or legal advice.
"""

from .rules import RULES, THRESHOLDS

__all__ = ["RULES", "THRESHOLDS"]
