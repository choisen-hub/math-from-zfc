#!/usr/bin/env python3
"""Cross-reference each phase of math-from-zfc with machine-verified theorems in Metamath's set.mm
(public domain, https://github.com/metamath/set.mm) and with Lean 4 / Mathlib declarations.

For every set.mm label listed below the script pulls the actual statement (and the first sentence of its
comment) out of set.mm, so nothing is quoted from memory, and writes docs/metamath-crosswalk.md with links
to the Metamath Proof Explorer (https://us.metamath.org/mpeuni/<label>.html).

Usage:
    python3 metamath_crosswalk.py                 # expects _ref/set.mm (download once, ~50 MB)
    curl -L -o _ref/set.mm https://raw.githubusercontent.com/metamath/set.mm/develop/set.mm
Optional full verification of set.mm with the reference verifier (slow, minutes):
    curl -L -o _ref/mmverify.py https://raw.githubusercontent.com/david-a-wheeler/mmverify.py/master/mmverify.py
    python3 _ref/mmverify.py _ref/set.mm
"""
import os, re, sys, datetime
HERE = os.path.dirname(os.path.abspath(__file__))
MM = os.path.join(HERE, "_ref", "set.mm")

# phase → (title, [(label, what it corresponds to in this project)])
PHASES = [
    ("Phase 1: ZFC axioms (phase01_zfc_axioms.py)", [
        ("ax-ext", "AxiomOfExtensionality"), ("ax-nul", "AxiomOfEmptySet (in set.mm a theorem-like axiom; derivable from ax-sep)"),
        ("ax-pr", "AxiomOfPairing"), ("ax-un", "AxiomOfUnion"), ("ax-pow", "AxiomOfPowerSet"),
        ("ax-sep", "AxiomSchemaOfSeparation"), ("ax-rep", "AxiomSchemaOfReplacement"), ("ax-inf", "AxiomOfInfinity"),
        ("ax-ac", "AxiomOfChoice (set.mm states it in Kuratowski's form)"), ("ax-reg", "AxiomOfFoundation (regularity)"),
        ("df-op", "Kuratowski ordered pair used in the pairing demonstration"), ("opthg", "ordered-pair equality theorem"),
        ("df-pw", "power set"), ("df-uni", "union of a class"),
    ]),
    ("Phase 2: natural numbers as von Neumann ordinals (phase02_natural_numbers.py)", [
        ("df-suc", "successor x ∪ {x} (VonNeumannOrdinal.successor)"), ("df-om", "omega, the set of natural numbers (finite ordinals)"),
        ("omsson", "omega is a subset of the ordinals"), ("peano1", "0 ∈ ω"), ("peano2", "successor stays in ω"),
        ("peano3", "0 is not a successor"), ("peano4", "successor is injective"), ("peano5", "induction (demonstrate_induction)"),
        ("findes", "finite induction scheme"), ("df-lim", "limit ordinal (contrast with successor ordinals)"),
    ]),
    ("Phase 3: arithmetic by recursion (phase03_arithmetic.py)", [
        ("df-rdg", "recursive definition generator: the theorem that justifies defining add/mul by recursion on the successor"),
        ("nnind", "induction over positive integers, used for the commutativity/associativity demonstrations"),
    ]),
    ("Phase 4 and 5: integers and rationals as equivalence classes (phase04_integers.py, phase05_rationals.py)", [
        ("df-ec", "equivalence class [a]R (Integer / Rational as classes of pairs)"), ("df-qs", "quotient set A/R"),
        ("df-ni", "positive integers as omega minus 0 (set.mm's own construction route)"), ("df-pli", "addition on positive integers"),
        ("df-mi", "multiplication on positive integers"), ("df-lti", "ordering on positive integers"),
        ("df-nq", "positive fractions: pairs of positive integers modulo the cross-multiplication relation (same idea as Rational)"),
        ("sqrt2irr", "square root of 2 is irrational (phase05 proof)"),
    ]),
    ("Phase 6: reals via Dedekind cuts (phase06_reals.py)", [
        ("df-np", "positive reals as Dedekind cuts of positive fractions (DedekindCut)"), ("df-nr", "signed reals as classes of pairs of positive reals"),
        ("df-c", "complex numbers; the real numbers are then carved out"), ("df-r", "the real numbers"),
        ("axsup", "completeness: least upper bound property (completeness demonstration)"), ("df-sup", "supremum"),
        ("dedekind", "Dedekind cut property of the reals"), ("ruc", "the reals are uncountable (Cantor's diagonal argument)"),
        ("canth", "Cantor's theorem: no set maps onto its power set"),
    ]),
    ("Phase 7: algebraic structures (phase07_algebraic_structures.py)", [
        ("df-grp", "group"), ("df-ring", "ring"), ("df-field", "field"), ("df-dvds", "divisibility (ℤ/nℤ examples)"),
    ]),
    ("Phase 8: analysis (phase08_analysis.py)", [
        ("df-clim", "limit of a sequence (ε-N definition)"), ("climrel", "the limit relation is a relation"), ("df-sqrt", "square root (used in the √2 example)"),
    ]),
]

LEAN = [
    ("ZFC itself", "Mathlib.SetTheory.ZFC.Basic", "ZFSet", "a model of ZFC sets inside Lean's type theory; the axioms appear as theorems such as ZFSet.ext, ZFSet.pair, ZFSet.sUnion, ZFSet.powerset, ZFSet.omega"),
    ("Phase 2", "Init.Prelude / Mathlib.Data.Nat.Basic", "Nat", "natural numbers as an inductive type (zero, succ); induction is Nat.rec. Mathlib also has the von Neumann route via ordinals: Mathlib.SetTheory.Ordinal.Basic"),
    ("Phase 3", "Mathlib.Data.Nat.Basic", "Nat.add, Nat.mul", "defined by structural recursion on succ; commutativity/associativity are Nat.add_comm, Nat.mul_comm, Nat.add_assoc"),
    ("Phase 4", "Init.Data.Int.Basic / Mathlib.Data.Int.Basic", "Int", "integers as an inductive type with two constructors (ofNat, negSucc) rather than as equivalence classes; the quotient-of-pairs construction is Mathlib.Data.Int.Defs comments and the general tool is Quotient"),
    ("Phase 5", "Mathlib.Data.Rat.Defs", "Rat", "rationals as reduced fractions (num, den, coprime proof); Rat.num_div_den etc."),
    ("Phase 6", "Mathlib.Data.Real.Basic", "Real", "reals as the Cauchy completion of ℚ (CauSeq.Completion.Cauchy), not Dedekind cuts; completeness is Real.exists_isLUB; Dedekind-style order facts are in Mathlib.Order.CompleteLattice"),
    ("Phase 7", "Mathlib.Algebra.Group.Defs, Mathlib.Algebra.Ring.Defs, Mathlib.Algebra.Field.Defs", "Group, Ring, Field", "typeclass definitions; ZMod n is Mathlib.Data.ZMod.Basic, the symmetric group is Equiv.Perm"),
    ("Phase 8", "Mathlib.Topology.Basic, Mathlib.Analysis.Calculus.Deriv.Basic", "Filter.Tendsto, ContinuousAt, HasDerivAt", "limits are expressed with filters; the ε-N and ε-δ forms are Metric.tendsto_atTop and Metric.continuousAt_iff"),
]

def load_statements(labels):
    if not os.path.exists(MM): sys.exit(f"set.mm not found at {MM}; see the docstring for the download command")
    t = open(MM, encoding="utf-8", errors="ignore").read()
    out = {}
    for lab in labels:
        m = re.search(r"\$\(\s*(.*?)\$\)\s*" + re.escape(lab) + r" \$([ap]) (.*?) \$[.=]", t, re.S)
        if not m:
            m2 = re.search(r"^\s*" + re.escape(lab) + r" \$([ap]) (.*?) \$[.=]", t, re.M | re.S)
            if not m2: out[lab] = None; continue
            out[lab] = ("", m2.group(1), re.sub(r"\s+", " ", m2.group(2)).strip()); continue
        comment = re.sub(r"\s+", " ", m.group(1)).strip()
        first = re.split(r"(?<=[.!?])\s", comment, 1)[0]
        out[lab] = (first[:220], m.group(2), re.sub(r"\s+", " ", m.group(3)).strip())
    return out

def main():
    labels = [lab for _, items in PHASES for lab, _ in items]
    st = load_statements(labels)
    missing = [l for l in labels if st[l] is None]
    lines = ["# Cross-reference: math-from-zfc, Metamath set.mm and Lean/Mathlib", "",
             f"Generated by `metamath_crosswalk.py` on {datetime.date.today()} from a local copy of set.mm. Statements below are copied from set.mm verbatim (ASCII notation: `A.` for all, `E.` exists, `e.` element of, `->` implies, `<->` iff, `/\\` and, `-.` not).",
             "Each label links to the Metamath Proof Explorer, where the complete machine-verified proof can be read.", ""]
    for title, items in PHASES:
        lines += [f"## {title}", "", "| set.mm | kind | corresponds to | statement |", "|---|---|---|---|"]
        for lab, what in items:
            s = st[lab]
            if s is None: lines.append(f"| `{lab}` | ? | {what} | (label not found in this set.mm) |"); continue
            kind = "axiom" if s[1] == "a" and lab.startswith("ax-") else "definition" if lab.startswith("df-") else "theorem"
            stmt = s[2].replace("|", "\\|")
            lines.append(f"| [`{lab}`](https://us.metamath.org/mpeuni/{lab}.html) | {kind} | {what} | `{stmt[:160]}{'…' if len(stmt) > 160 else ''}` |")
        lines.append("")
    lines += ["## Lean 4 / Mathlib", "", "Mathlib does not build the number systems from ZFC; it builds them inside Lean's type theory. The table says where each phase's objects live there and how the construction differs.", "",
              "| phase | module | declaration | note |", "|---|---|---|---|"]
    for ph, mod, decl, note in LEAN:
        lines.append(f"| {ph} | `{mod}` | `{decl}` | {note} |")
    lines += ["", "Documentation: https://leanprover-community.github.io/mathlib4_docs/ (search by declaration name).", "",
              "## Where this project departs from the verified route", "",
              "- set.mm goes positive integers (df-ni) → positive fractions (df-nq) → positive reals as Dedekind cuts (df-np) → signed reals (df-nr) → complex numbers (df-c) and only then defines ℝ as a subset. This project goes ℕ → ℤ → ℚ → ℝ, the textbook order. Both are legitimate; the set.mm order avoids defining subtraction before the reals exist.",
              "- Phase 3 computes with Python `int` while printing the successor unfolding, and phase 8 uses `float`. The corresponding set.mm theorems (df-rdg, df-clim) show what a fully formal version would need.",
              "- Lean's Nat, Int and Rat are inductive types, not sets; the equivalence-class constructions in phases 4 and 5 correspond to Lean's general `Quotient` machinery rather than to the concrete definitions of Int and Rat."]
    os.makedirs(os.path.join(HERE, "docs"), exist_ok=True)
    out = os.path.join(HERE, "docs", "metamath-crosswalk.md")
    open(out, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print(f"wrote {os.path.relpath(out, HERE)}: {len(labels)} labels, {len(missing)} missing {missing}")

if __name__ == "__main__":
    main()
