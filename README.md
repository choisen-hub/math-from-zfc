# math-from-zfc

math-from-zfc is a set of Python modules that build the number systems and basic structures of mathematics step by step from the ZFC axioms (Zermelo-Fraenkel set theory with the axiom of choice): the natural numbers as von Neumann ordinals, arithmetic by recursion, integers and rationals as equivalence classes of pairs, reals as Dedekind cuts, then groups, rings and fields, and finally limits, continuity and derivatives. Each module is written so that the docstrings are the textbook and the code is the worked demonstration; running a module prints an interactive walkthrough. A standalone HTML page summarizes the same journey with a few in-browser calculators.

It is a learning project for a reader at roughly first-year university level who wants to see what "mathematics is built on sets" means in practice. All docstrings, printed output and the HTML page are in Korean.

The Korean version of this document is in `README.ko.md`.

## Features

- Nine phase modules, one per topic, each runnable on its own with `python phaseNN_*.py` and ending in an `if __name__ == "__main__":` demonstration.
- A strict linear dependency rule: a phase may import only earlier phases. The chain is phase01 <- phase02 <- phase03 <- phase04 <- phase05 <- phase06, with phase07 importing phase04 and phase05, phase08 standing alone, and phase09 importing only `utils`.
- Phase 1 (`phase01_zfc_axioms.py`): one class per axiom (extensionality, empty set, pairing, union, power set, separation schema, replacement schema, infinity, choice, foundation), each with a long explanatory docstring and a `demonstrate()` method that simulates the axiom with Python `frozenset` values (for example, Kuratowski ordered pairs built from the pairing axiom).
- Phase 2 (`phase02_natural_numbers.py`): `VonNeumannOrdinal` keeps the actual nested `frozenset` representation of each number (0 = ∅, 1 = {∅}, 2 = {∅, {∅}}, ...) with a cache, and `NaturalNumber` builds on it; demonstrations of order as membership and of induction.
- Phase 3 (`phase03_arithmetic.py`): `add` and `mul` defined by recursion on the successor, with a `verbose` mode that prints every unfolding step, plus demonstrations of commutativity, associativity, distributivity and the interaction with order.
- Phase 4 (`phase04_integers.py`): integers as equivalence classes of pairs of naturals under (a, b) ~ (c, d) iff a + d = b + c, verification that this is an equivalence relation, an `Integer` class with arithmetic, and the embedding of ℕ into ℤ.
- Phase 5 (`phase05_rationals.py`): the same pattern with multiplication, a `Rational` class, the embedding of ℤ into ℚ, a density demonstration, and a proof that √2 is irrational.
- Phase 6 (`phase06_reals.py`): `DedekindCut` represented by a predicate on rationals (so an infinite set is handled through the separation schema rather than stored), cuts for rationals, √2 and π, a completeness demonstration (least upper bound) and Cantor's diagonal argument.
- Phase 7 (`phase07_algebraic_structures.py`): `Group`, `Ring` and `Field` classes that check their axioms on finite examples (ℤ/nℤ, the symmetric group S3, the field ℤ/5ℤ) and a homomorphism demonstration.
- Phase 8 (`phase08_analysis.py`): a `Sequence` class, an ε-N convergence checker, demonstrations of limit theorems, ε-δ continuity and the derivative, and a text-based ε-band table that shows a sequence entering successively narrower bands.
- Phase 9 (`phase09_overview.py`): prints the whole journey, a table of which ZFC axiom was used where, the recurring patterns, the limits of the approach and possible next steps, then saves `dependency_graph.png`.
- `utils/dependency_graph.py`: a hand-maintained list of concept nodes and edges rendered with matplotlib, with a lookup for a Korean font (AppleGothic, Apple SD Gothic Neo, NanumGothic or Malgun Gothic) so labels render correctly, and a printed dependency table.
- `index.html`: a self-contained page (no external scripts) with one section per phase and three interactive calculators written in plain JavaScript: the von Neumann set expansion of a number, the step-by-step recursive computation of a + b, and the equivalence class of an integer.

## How it works

```
phase01_zfc_axioms.py        axioms as classes with demonstrate()
        ^
phase02_natural_numbers.py   von Neumann ordinals as nested frozensets
        ^
phase03_arithmetic.py        add / mul by recursion on successor
        ^
phase04_integers.py          Integer = equivalence class of (a, b)
        ^
phase05_rationals.py         Rational = equivalence class of (a, b), b != 0
        ^                 ^
phase06_reals.py          phase07_algebraic_structures.py
DedekindCut(predicate)    Group / Ring / Field over finite examples

phase08_analysis.py          limits, continuity, derivative (uses only math)
phase09_overview.py          summary + utils/dependency_graph.py -> dependency_graph.png
index.html                   static companion page with JS calculators
```

Inside each phase the constructions are literal where that is practical (nested frozensets for ordinals, pairs for integers and rationals, predicates for cuts) and switch to ordinary Python integers and floats where a literal encoding would be unreadable (recursive arithmetic in phase 3 operates on `int` while printing the successor-unfolding steps; phase 8 uses floats). The docstrings say which choice was made and why.

## Requirements

- Python 3.8 or later (the code uses f-strings and type hints only from the standard library).
- `matplotlib`, only for `utils/dependency_graph.py` and the final step of `phase09_overview.py`. Every other phase runs without third-party packages.
- A Korean-capable font if you regenerate the dependency graph; the script looks for AppleGothic, Apple SD Gothic Neo, NanumGothic or Malgun Gothic and otherwise leaves matplotlib's default, in which case Korean labels may render as boxes.

## Installation and running

```bash
git clone https://github.com/choisen-hub/math-from-zfc.git
cd math-from-zfc

# optional, for the dependency graph only
python3 -m venv venv
./venv/bin/pip install matplotlib
```

Run the phases in order, or any one of them:

```bash
python3 phase01_zfc_axioms.py
python3 phase02_natural_numbers.py
python3 phase03_arithmetic.py
python3 phase04_integers.py
python3 phase05_rationals.py
python3 phase06_reals.py
python3 phase07_algebraic_structures.py
python3 phase08_analysis.py
python3 phase09_overview.py        # also writes dependency_graph.png
```

Regenerate only the graph:

```bash
python3 utils/dependency_graph.py
```

Open the companion page directly in a browser; it needs no server:

```bash
open index.html
```

Run the scripts from the repository root so that the `from phaseNN_... import ...` lines resolve.

## Configuration

There are no environment variables or configuration files.

- The concept nodes and edges of the graph are the `NODES` and `EDGES` lists at the top of `utils/dependency_graph.py`.
- The output path of the graph is fixed to `dependency_graph.png` in the repository root by both `phase09_overview.py` and `utils/dependency_graph.py`.
- The font candidates for Korean labels are listed in `utils/dependency_graph.py`.

## Project structure

```
math-from-zfc/
  phase01_zfc_axioms.py            the ten ZFC axioms as documented classes
  phase02_natural_numbers.py       von Neumann ordinals, NaturalNumber, order, induction
  phase03_arithmetic.py            recursive addition and multiplication, their laws
  phase04_integers.py              Integer as equivalence class, embedding of N
  phase05_rationals.py             Rational as equivalence class, density, sqrt(2) irrational
  phase06_reals.py                 DedekindCut, completeness, diagonal argument
  phase07_algebraic_structures.py  Group, Ring, Field with finite examples
  phase08_analysis.py              Sequence, epsilon-N, continuity, derivative
  phase09_overview.py              retrospective, axiom usage table, graph generation
  utils/
    __init__.py
    dependency_graph.py            matplotlib rendering of the concept graph
  dependency_graph.png             generated graph (checked in)
  index.html                       static companion page with JS calculators
  LICENSE
  README.md                        this file
  README.ko.md                     Korean version
```

## Usage examples

Use the modules interactively:

```python
from phase02_natural_numbers import NaturalNumber
from phase03_arithmetic import add, mul
from phase04_integers import Integer
from phase05_rationals import Rational
from phase06_reals import cut_sqrt2, cut_rational

three = NaturalNumber(3)          # holds the frozenset {∅, {∅}, {∅, {∅}}}
add(2, 3, verbose=True)           # prints each successor-unfolding step, returns 5
Integer(-3)                       # stored as the class of the pair (0, 3)
Rational(3, 4)                    # the class of the pair (3, 4); denominator 0 raises
cut_sqrt2()                       # a DedekindCut whose lower set is {q : q < 0 or q^2 < 2}
```

Read a phase as a text. The docstring at the top of each file gives the motivation, the formal statement, the "what breaks without this" argument and the connection to the previous phase; the demonstration at the bottom prints the same ideas with concrete values.

## Data, licensing and attribution

- The constructions follow the standard textbook route (von Neumann ordinals, Grothendieck-style pairs for ℤ and ℚ, Dedekind cuts for ℝ). No external datasets are used.
- `dependency_graph.png` is generated by the code in this repository.
- The HTML page uses no third-party libraries or fonts.

## Cross-reference with verified mathematics

`python3 metamath_crosswalk.py` generates `docs/metamath-crosswalk.md`: for each phase, the Metamath set.mm axioms, definitions and theorems that correspond to the construction (statements copied from set.mm, links to the machine-verified proofs on the Metamath Proof Explorer), plus the Lean 4 / Mathlib declarations where the same objects live and a note on where this project's route differs from the verified one. set.mm is downloaded to `_ref/` (ignored by git); the docstring in the script has the commands.

## Known limitations and roadmap

- Everything is in Korean; there is no English text in the modules or the page.
- The demonstrations are simulations, not formal proofs: Python checks finite examples (for instance, group axioms on ℤ/5ℤ) and prints arguments, it does not verify them.
- Phases 3 and 8 use Python `int` and `float` rather than the set-theoretic objects from earlier phases, for readability.
- `DedekindCut` can represent a real only when you can write a rational predicate for it; cuts for arbitrary reals are not constructible here.
- Planned extensions listed in `phase09_overview.py` and the Korean README: complex numbers, Cantor's set theory, Gödel's incompleteness theorems, a Lean 4 port, and non-Euclidean geometry. None of these exist yet.

## License

MIT. See [LICENSE](LICENSE).
