"""Tests for MöbiusNumber — complementary residue arithmetic."""

import pytest
from fractions import Fraction
from mobius_number import MobiusNumber, M


# =====================================================================
# THE PROOF: 0.1 + 0.2 = 0.3
# =====================================================================

class TestTheProof:
    """The problem that started it all."""

    def test_ieee754_fails(self):
        """IEEE 754 gets this wrong. This is not a bug — it's the spec."""
        assert 0.1 + 0.2 != 0.3  # The 41-year-old problem

    def test_mobius_solves_it(self):
        """MöbiusNumber gets it right."""
        assert M("0.1") + M("0.2") == M("0.3")

    def test_collapse_is_exact(self):
        result = M("0.1") + M("0.2")
        assert result.collapse() == 0.3

    def test_error_is_zero(self):
        result = M("0.1") + M("0.2")
        target = M("0.3")
        assert result.exact - target.exact == Fraction(0)


# =====================================================================
# CONSTRUCTION
# =====================================================================

class TestConstruction:
    """Every input path must produce the correct rational strand."""

    def test_from_string(self):
        n = M("0.1")
        assert n.exact == Fraction(1, 10)

    def test_from_int(self):
        n = M(42)
        assert n.exact == Fraction(42)
        assert n.approx == 42.0

    def test_from_float(self):
        n = M(0.5)
        assert n.exact == Fraction(1, 2)

    def test_from_fraction(self):
        n = M(Fraction(1, 7))
        assert n.exact == Fraction(1, 7)

    def test_from_mobius(self):
        a = M("3.14")
        b = M(a)
        assert b.exact == a.exact

    def test_from_negative_string(self):
        n = M("-0.1")
        assert n.exact == Fraction(-1, 10)

    def test_from_zero(self):
        n = M(0)
        assert n.exact == Fraction(0)
        assert n.approx == 0.0

    def test_invalid_type_raises(self):
        with pytest.raises(TypeError):
            M([1, 2, 3])


# =====================================================================
# ARITHMETIC
# =====================================================================

class TestArithmetic:
    """Both strands must propagate through every operation."""

    def test_addition(self):
        assert (M("0.1") + M("0.2")).exact == Fraction(3, 10)

    def test_subtraction(self):
        assert (M("0.3") - M("0.1")).exact == Fraction(1, 5)

    def test_multiplication(self):
        assert (M("0.1") * M("10")).exact == Fraction(1)

    def test_division(self):
        assert (M("1") / M("3")).exact == Fraction(1, 3)

    def test_negation(self):
        assert (-M("0.5")).exact == Fraction(-1, 2)

    def test_abs(self):
        assert abs(M("-7")).exact == Fraction(7)

    def test_power(self):
        assert (M("3") ** 2).exact == Fraction(9)

    def test_division_by_zero(self):
        with pytest.raises(ZeroDivisionError):
            M("1") / M("0")

    def test_radd(self):
        result = 1 + M("0.5")
        assert result.exact == Fraction(3, 2)

    def test_rsub(self):
        result = 1 - M("0.3")
        assert result.exact == Fraction(7, 10)

    def test_rmul(self):
        result = 3 * M("0.1")
        assert result.exact == Fraction(3, 10)

    def test_rtruediv(self):
        result = 1 / M("3")
        assert result.exact == Fraction(1, 3)


# =====================================================================
# THE FAMOUS FAILURES
# =====================================================================

class TestFamousFailures:
    """Every classic IEEE 754 failure, corrected."""

    def test_sum_point_one_ten_times(self):
        """0.1 added 10 times should equal 1.0."""
        total = M("0.0")
        for _ in range(10):
            total = total + M("0.1")
        assert total == M("1.0")

    def test_one_forty_ninth_times_forty_nine(self):
        """(1/49) * 49 should equal 1."""
        assert (M("1") / M("49")) * M("49") == M("1")

    def test_one_third_times_three(self):
        """(1/3) * 3 should equal 1."""
        assert (M("1") / M("3")) * M("3") == M("1")

    def test_ten_divided_by_three_times_three(self):
        """$10.00 / 3 * 3 should equal $10.00."""
        assert (M("10") / M("3")) * M("3") == M("10")

    def test_catastrophic_cancellation(self):
        """(1 + 1e-16) - 1 should equal 1e-16, not 0."""
        result = (M("1") + M("0.0000000000000001")) - M("1")
        assert result.exact == Fraction(1, 10**16)
        assert result.collapse() == 1e-16

    def test_ieee_catastrophic_cancellation_loses(self):
        """IEEE 754 loses this entirely — returns 0."""
        assert (1.0 + 1e-16) - 1.0 == 0.0  # Total information loss

    def test_one_seventh_round_trip(self):
        """1/7 * 7 = 1 exactly."""
        assert (M("1") / M("7")) * M("7") == M("1")

    def test_penny_accumulation(self):
        """Add $0.01 one hundred times = $1.00."""
        total = M("0.0")
        for _ in range(100):
            total = total + M("0.01")
        assert total == M("1.0")


# =====================================================================
# COMPARISON — THE RATIONAL GOVERNS
# =====================================================================

class TestComparison:
    """Equality and ordering use the rational strand, not the float."""

    def test_equality(self):
        assert M("0.1") == M("0.1")

    def test_inequality(self):
        assert M("0.1") != M("0.2")

    def test_less_than(self):
        assert M("0.1") < M("0.2")

    def test_less_equal(self):
        assert M("0.1") <= M("0.1")
        assert M("0.1") <= M("0.2")

    def test_greater_than(self):
        assert M("0.2") > M("0.1")

    def test_greater_equal(self):
        assert M("0.2") >= M("0.2")
        assert M("0.2") >= M("0.1")

    def test_cross_type_equality(self):
        assert M("5") == M(5)

    def test_hash_consistency(self):
        """Equal MöbiusNumbers must have equal hashes."""
        a = M("0.1") + M("0.2")
        b = M("0.3")
        assert hash(a) == hash(b)

    def test_usable_as_dict_key(self):
        d = {M("0.3"): "found"}
        key = M("0.1") + M("0.2")
        assert d[key] == "found"


# =====================================================================
# STRAND ANATOMY
# =====================================================================

class TestStrands:
    """The residue (anti-strand) must be the exact complement."""

    def test_residue_of_point_one(self):
        n = M("0.1")
        # residue = exact - Fraction(approx)
        # exact is 1/10, approx is the nearest float
        assert n.residue == Fraction(1, 10) - Fraction(0.1)

    def test_residue_of_integer_is_zero(self):
        n = M(1)
        assert n.residue == Fraction(0)

    def test_residue_of_half_is_zero(self):
        n = M("0.5")
        assert n.residue == Fraction(0)  # 0.5 is exact in binary

    def test_diagnose_returns_dict(self):
        d = M("0.1").diagnose()
        assert "binary_strand" in d
        assert "rational_strand" in d
        assert "residue" in d
        assert "collapsed" in d


# =====================================================================
# DISPLAY
# =====================================================================

class TestDisplay:
    """String output must show the collapsed (exact) value."""

    def test_str(self):
        assert str(M("0.3")) == "0.3"

    def test_repr(self):
        assert repr(M("0.1")) == "M('1/10')"

    def test_float_conversion(self):
        assert float(M("0.5")) == 0.5

    def test_int_conversion(self):
        assert int(M("42")) == 42


# =====================================================================
# ACCUMULATION STRESS
# =====================================================================

class TestAccumulation:
    """Errors must not compound across long chains."""

    def test_thousand_additions(self):
        """0.001 * 1000 = 1.0 exactly."""
        total = M("0.0")
        for _ in range(1000):
            total = total + M("0.001")
        assert total == M("1.0")

    def test_chained_division_multiplication(self):
        """(((1 / 3) / 7) / 11) * 11 * 7 * 3 = 1."""
        n = M("1")
        n = n / M("3")
        n = n / M("7")
        n = n / M("11")
        n = n * M("11")
        n = n * M("7")
        n = n * M("3")
        assert n == M("1")

    def test_financial_chain(self):
        """$100 split 7 ways, then reassembled."""
        share = M("100") / M("7")
        total = share * M("7")
        assert total == M("100")
