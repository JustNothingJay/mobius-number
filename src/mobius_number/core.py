"""
MöbiusNumber core implementation.

A number that carries its own correction. Two strands — the binary
approximation and the exact rational identity — coexist as one object.
On collapse, the rational governs.

The structure mirrors DNA: every base carries its complement.
The topology is Möbius: traversing the full loop returns the exact value.
"""

from fractions import Fraction
from typing import Union


class MobiusNumber:
    """
    A number that carries its own correction.

    Internally:
      _approx  : float    — the binary strand (fast, lossy)
      _exact   : Fraction  — the anti strand (exact, complete)

    The float is the shadow. The Fraction is the substance.
    Collapse = the Möbius traversal → exact output.

    Construction:
      MobiusNumber("0.1")      — from string (purest: "0.1" means exactly 1/10)
      MobiusNumber(0.1)        — from float (recovers rational intent)
      MobiusNumber(1)          — from int (exact)
      MobiusNumber(Fraction(1, 10))  — from Fraction (exact)
    """

    __slots__ = ('_approx', '_exact')

    def __init__(self, value: Union[int, float, str, Fraction, 'MobiusNumber']):
        if isinstance(value, MobiusNumber):
            self._approx = value._approx
            self._exact = value._exact
        elif isinstance(value, Fraction):
            self._exact = value
            self._approx = float(value)
        elif isinstance(value, int):
            self._exact = Fraction(value)
            self._approx = float(value)
        elif isinstance(value, float):
            self._approx = value
            self._exact = Fraction(value).limit_denominator(10**15)
        elif isinstance(value, str):
            self._exact = Fraction(value)
            self._approx = float(self._exact)
        else:
            raise TypeError(f"Cannot create MobiusNumber from {type(value)}")

    # ------------------------------------------------------------------
    # Strand access
    # ------------------------------------------------------------------

    @property
    def approx(self) -> float:
        """The binary strand — hardware-fast, carries rounding error."""
        return self._approx

    @property
    def exact(self) -> Fraction:
        """The rational strand — exact, no loss."""
        return self._exact

    @property
    def residue(self) -> Fraction:
        """The anti-strand: exact_value − binary_approximation."""
        return self._exact - Fraction(self._approx)

    # ------------------------------------------------------------------
    # Collapse — the Möbius traversal
    # ------------------------------------------------------------------

    def collapse(self) -> float:
        """
        Traverse the full Möbius loop.
        Binary approximation + anti-strand residue → exact value.
        """
        return float(self._exact)

    # ------------------------------------------------------------------
    # Arithmetic — both strands propagate
    # ------------------------------------------------------------------

    def __add__(self, other):
        other = _coerce(other)
        result = MobiusNumber.__new__(MobiusNumber)
        result._exact = self._exact + other._exact
        result._approx = self._approx + other._approx
        return result

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        other = _coerce(other)
        result = MobiusNumber.__new__(MobiusNumber)
        result._exact = self._exact - other._exact
        result._approx = self._approx - other._approx
        return result

    def __rsub__(self, other):
        other = _coerce(other)
        return other.__sub__(self)

    def __mul__(self, other):
        other = _coerce(other)
        result = MobiusNumber.__new__(MobiusNumber)
        result._exact = self._exact * other._exact
        result._approx = self._approx * other._approx
        return result

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        other = _coerce(other)
        if other._exact == 0:
            raise ZeroDivisionError("MobiusNumber division by zero")
        result = MobiusNumber.__new__(MobiusNumber)
        result._exact = self._exact / other._exact
        result._approx = self._approx / other._approx
        return result

    def __rtruediv__(self, other):
        other = _coerce(other)
        return other.__truediv__(self)

    def __neg__(self):
        result = MobiusNumber.__new__(MobiusNumber)
        result._exact = -self._exact
        result._approx = -self._approx
        return result

    def __abs__(self):
        result = MobiusNumber.__new__(MobiusNumber)
        result._exact = abs(self._exact)
        result._approx = abs(self._approx)
        return result

    def __pow__(self, exp):
        if isinstance(exp, int):
            result = MobiusNumber.__new__(MobiusNumber)
            result._exact = self._exact ** exp
            result._approx = self._approx ** exp
            return result
        return NotImplemented

    # ------------------------------------------------------------------
    # Comparison — the rational governs, always
    # ------------------------------------------------------------------

    def __eq__(self, other):
        if not isinstance(other, (MobiusNumber, int, float, str, Fraction)):
            return NotImplemented
        other = _coerce(other)
        return self._exact == other._exact

    def __ne__(self, other):
        if not isinstance(other, (MobiusNumber, int, float, str, Fraction)):
            return NotImplemented
        other = _coerce(other)
        return self._exact != other._exact

    def __lt__(self, other):
        other = _coerce(other)
        return self._exact < other._exact

    def __le__(self, other):
        other = _coerce(other)
        return self._exact <= other._exact

    def __gt__(self, other):
        other = _coerce(other)
        return self._exact > other._exact

    def __ge__(self, other):
        other = _coerce(other)
        return self._exact >= other._exact

    # ------------------------------------------------------------------
    # Display
    # ------------------------------------------------------------------

    def __repr__(self):
        return f"M('{self._exact}')"

    def __str__(self):
        return str(float(self._exact))

    def __float__(self):
        return float(self._exact)

    def __int__(self):
        return int(self._exact)

    def __hash__(self):
        return hash(self._exact)

    # ------------------------------------------------------------------
    # Diagnostic
    # ------------------------------------------------------------------

    def diagnose(self) -> dict:
        """Return both strands and the residue between them."""
        return {
            "binary_strand": self._approx,
            "rational_strand": str(self._exact),
            "residue": str(self.residue),
            "residue_float": float(self.residue),
            "collapsed": self.collapse(),
        }


def _coerce(value) -> MobiusNumber:
    """Convert a raw value into a MobiusNumber."""
    if isinstance(value, MobiusNumber):
        return value
    return MobiusNumber(value)
