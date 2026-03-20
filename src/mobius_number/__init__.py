"""
MöbiusNumber — Complementary Residue Arithmetic

Every number is stored as two strands:
  - The binary approximation (float64, hardware-fast)
  - The exact rational identity (numerator/denominator, no loss)

They are not two representations. They are one object — like DNA's
double helix, like a Möbius strip traversed fully. The approximation
and its anti coexist. On collapse, the rational governs.

The float gives you speed.
The rational gives you truth.
Collapse gives you both.

    >>> from mobius_number import M
    >>> M("0.1") + M("0.2") == M("0.3")
    True

Jay Carpenter, 2026
"""

from mobius_number.core import MobiusNumber

# Convenience alias
M = MobiusNumber

__version__ = "0.1.0"
__all__ = ["MobiusNumber", "M"]
