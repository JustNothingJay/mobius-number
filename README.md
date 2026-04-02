                                          - 1 ++ # MöbiusNumber

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19154816.svg)](https://doi.org/10.5281/zenodo.19154816)

**0.1 + 0.2 = 0.3. Exactly.**

```python
from mobius_number import M

>>> 0.1 + 0.2 == 0.3
False

>>> M("0.1") + M("0.2") == M("0.3")
True
```

A number type that carries its own correction. No rounding error. No epsilon comparisons. No workarounds.

## Install

```
pip install mobius-number
```

## The Problem

Every computer in the world gets this wrong:

```python
>>> 0.1 + 0.2
0.30000000000000004

>>> 0.1 + 0.2 == 0.3
False
```

This has been true since 1985 when IEEE 754 was published. The reason: computers store numbers in base 2. The number 0.1 in binary is a repeating fraction — like 1/3 in decimal (0.333...). It gets rounded. Then 0.2 gets rounded. The rounding errors stack.

Every workaround — arbitrary precision, interval arithmetic, posit numbers — tries to fix the math layer while leaving the foundation untouched: the number is stored in the form the transistor speaks, and the human adapts.

**What if the representation served the number instead?**

## The Idea

DNA has two strands. Every base carries its complement — A pairs with T, G pairs with C. There is no excess. The complement consumes what the original doesn't cover.

A Möbius strip has one surface. Traversing the full loop covers both "sides" and returns to the origin.

A MöbiusNumber stores two strands:

- **The binary strand** — `float64`, hardware-fast, carries rounding error
- **The rational strand** — exact `Fraction`, no loss, no repeating

They are not two separate representations. They are one object. The binary strand is the shadow. The rational strand is the substance. **On collapse, the rational governs.**

```
CURRENT (IEEE 754):
  Store 0.1 → 0.1000000000000000055511...
  Residue:     0.0000000000000000055511...  ← THROWN AWAY

MöbiusNumber:
  Binary strand:   0.1000000000000000055511...
  Rational strand: 1/10
  Anti (residue):  exact_value − binary_value
  Collapse:        the rational governs → 0.1 exactly
```

Arithmetic propagates both strands. When you add two MöbiusNumbers, the rationals add exactly. The floats add approximately. **The error exists but is never consulted for truth.** The anti-strand is always present, always correct, and annihilates the rounding error on collapse.

## Proof

```
$ python -c "from mobius_number import M; print(M('0.1') + M('0.2') == M('0.3'))"
True
```

### The Famous Failures — All Fixed

| Test | IEEE 754 | MöbiusNumber |
|------|----------|--------------|
| `0.1 + 0.2 == 0.3` | **False** | **True** |
| `(1/49) * 49 == 1` | **False** | **True** |
| `(1 + 1e-16) - 1` | **0.0** (total loss) | **1e-16** (exact) |
| `0.1 * 10 == 1.0` | True¹ | True |
| `$10 / 3 * 3 == $10` | True¹ | True |
| `0.01 * 100 == 1.0` | True¹ | True |
| `(1/7) * 7 == 1` | **False** | **True** |
| `0.001 added 1000×` | **False** | **True** |

¹ IEEE 754 gets these by luck — the rounding errors happen to cancel. The MöbiusNumber gets them by construction.

### Strand Anatomy

```python
from mobius_number import M

n = M("0.1")
print(n.diagnose())
# {
#   'binary_strand': 0.1,
#   'rational_strand': '1/10',
#   'residue': '-1/180143985094819840',
#   'residue_float': -5.55e-18,
#   'collapsed': 0.1
# }
```

The residue is the anti-strand — the exact complement of the binary error. It exists. It is never discarded. On collapse, the Möbius strip closes.

## Usage

```python
from mobius_number import M

# Basic arithmetic
a = M("0.1")
b = M("0.2")
c = a + b          # M('3/10')
c.collapse()        # 0.3

# Financial
price = M("19.99")
tax = price * M("0.0825")
total = price + tax  # Exact

# Comparison — the rational governs
M("0.1") + M("0.2") == M("0.3")  # True — always

# Interop with plain numbers
M("0.5") + 1        # M('3/2')
3 * M("0.1")         # M('3/10')

# Inspect the strands
n = M("0.1")
n.approx             # 0.1 (the float — fast, lossy)
n.exact              # Fraction(1, 10) (the truth)
n.residue            # Fraction(-1, 180143985094819840)
```

## Why Not Just Use `Fraction`?

You can. Python's `fractions.Fraction` gives exact rational arithmetic. But:

1. **Speed** — MöbiusNumber carries a float for fast approximate work. Use `.approx` in hot loops, `.collapse()` when you need truth.
2. **Drop-in intent** — `M("0.1")` reads like a number. `Fraction("0.1")` reads like a workaround.
3. **The conceptual point** — the number and its correction are one object. The anti-strand is not a separate operation. It is intrinsic. Like DNA. Like a Möbius strip.

## How It Works

Every MöbiusNumber is internally:

```
(_approx: float, _exact: Fraction)
```

- **Construction from string**: `M("0.1")` → `_exact = Fraction("0.1") = 1/10`; `_approx = float(1/10)`
- **Construction from float**: `M(0.1)` → recovers the rational intent via `limit_denominator`
- **Arithmetic**: both strands propagate independently through `+`, `-`, `*`, `/`, `**`
- **Comparison**: always uses `_exact` — the rational strand governs all equality and ordering
- **Collapse**: `float(_exact)` — the Möbius traversal returns the exact value

No external dependencies. Pure Python. Works on 3.9+.

## The Name

A Möbius strip is a surface with one side. If you trace a line along it, you cover both "sides" and return to the origin having traversed the whole thing. There is no front and back — only one continuous surface.

A MöbiusNumber is a number with one identity. The binary approximation and the exact rational are not two things — they are one object that, when fully traversed, resolves to the truth. The representation IS the correction.

## Author

Jay Carpenter — [SECS Research](https://github.com/JustNothingJay/SECS_Research)

## See Also

- [mobius-constant](https://github.com/JustNothingJay/mobius-constant) — Exact irrational constants (`sqrt(2)**2 == 2`, by construction)
- [mobius-integer](https://github.com/JustNothingJay/mobius-integer) — Dual-strand integer: machine i64 + exact BigInt (Rust)
- [mobius-units](https://github.com/JustNothingJay/mobius-units) — Fundamental constants from the eigenvalue tower — one measurement derives them all

Same pattern. Same anatomy. Same fix. Different domain.

## License

MIT
