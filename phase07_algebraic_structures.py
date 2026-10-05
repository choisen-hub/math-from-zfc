"""
Phase 7: 대수 구조 — 반복되는 패턴을 추상화하기
================================================

Phase 2-6에서 반복적으로 나타난 패턴이 있습니다:
    - 어떤 집합이 있다
    - 그 위에 연산이 있다
    - 연산이 결합법칙을 만족한다
    - 항등원이 있다
    - 역원이 있을 수도, 없을 수도 있다

이 패턴 자체를 연구 대상으로 삼는 것이 **추상대수학**입니다.

추상화의 위력:
    구체적 대상(ℤ, ℚ, ℝ)에서 공통 구조를 추출하여,
    그 구조(군, 환, 체) 수준에서 한 번 증명하면
    모든 구체적 사례에 한꺼번에 적용됩니다.

    라이프니츠가 꿈꿨던 보편 기호의 정신:
    구체적 내용을 기호로 추상화하고,
    기호 수준에서 추론하면
    모든 구체적 사례에 자동으로 적용됩니다.
"""

from phase04_integers import Integer
from phase05_rationals import Rational


# ============================================================================
#  군 (Group)
# ============================================================================

class Group:
    """
    군(Group): 가장 기본적인 대수 구조.

    정의:
        집합 G와 이항연산 ·: G × G → G의 쌍 (G, ·)이 다음을 만족할 때:

        (G1) 결합법칙: (a · b) · c = a · (b · c)
            "괄호 위치가 중요하지 않다"

        (G2) 항등원 존재: ∃e ∈ G, ∀a ∈ G, e · a = a · e = a
            "아무것도 하지 않는 연산이 있다"

        (G3) 역원 존재: ∀a ∈ G, ∃a⁻¹ ∈ G, a · a⁻¹ = a⁻¹ · a = e
            "모든 연산을 되돌릴 수 있다"

    추가로 교환법칙이 성립하면 아벨군(Abelian group):
        (G4) 교환법칙: a · b = b · a

    우리가 이미 본 예시:
        - (ℤ, +): 정수와 덧셈. Phase 4에서 구성한 것!
          항등원: 0, 역원: -n
        - (ℚ\\{0}, ×): 0이 아닌 유리수와 곱셈. Phase 5에서 구성한 것!
          항등원: 1, 역원: 1/a

    군 이론의 기본 정리:
        1. 항등원은 유일하다
        2. 역원은 유일하다
        이 두 정리를 "군" 수준에서 한 번 증명하면,
        ℤ, ℚ\\{0}, 대칭군, ... 모든 군에 적용된다!
    """

    def __init__(self, elements, operation, identity, inverse_fn, name="G"):
        """
        유한 군을 구성합니다.

        elements: 원소들의 리스트
        operation: 이항연산 함수 (a, b) → a · b
        identity: 항등원
        inverse_fn: 역원 함수 a → a⁻¹
        """
        self.elements = list(elements)
        self.op = operation
        self.identity = identity
        self.inv = inverse_fn
        self.name = name

    def verify_axioms(self) -> bool:
        """군 공리 (G1)-(G3)을 검증합니다."""
        E = self.elements

        # (G1) 결합법칙
        for a in E:
            for b in E:
                for c in E:
                    if self.op(self.op(a, b), c) != self.op(a, self.op(b, c)):
                        print(f"  ✗ 결합법칙 실패: ({a}·{b})·{c} ≠ {a}·({b}·{c})")
                        return False
        print(f"  ✓ (G1) 결합법칙")

        # (G2) 항등원
        e = self.identity
        for a in E:
            if self.op(e, a) != a or self.op(a, e) != a:
                print(f"  ✗ 항등원 실패: e·{a} ≠ {a} 또는 {a}·e ≠ {a}")
                return False
        print(f"  ✓ (G2) 항등원: {e}")

        # (G3) 역원
        for a in E:
            a_inv = self.inv(a)
            if self.op(a, a_inv) != e or self.op(a_inv, a) != e:
                print(f"  ✗ 역원 실패: {a}·{a_inv} ≠ {e}")
                return False
        print(f"  ✓ (G3) 역원 존재")

        return True

    def is_abelian(self) -> bool:
        """교환법칙이 성립하는지 검증합니다."""
        for a in self.elements:
            for b in self.elements:
                if self.op(a, b) != self.op(b, a):
                    return False
        return True

    def cayley_table(self):
        """케일리 표(연산표)를 출력합니다."""
        E = self.elements
        width = max(len(str(e)) for e in E) + 1

        header = " · |" + "|".join(f"{e!s:>{width}}" for e in E)
        print(f"  {header}")
        print(f"  {'─' * len(header)}")
        for a in E:
            row = f"{a!s:>2} |" + "|".join(
                f"{self.op(a, b)!s:>{width}}" for b in E
            )
            print(f"  {row}")


# ============================================================================
#  군의 구체적 예시들
# ============================================================================

def example_integers_mod_n(n: int) -> Group:
    """
    예시: 시계 산술 ℤ/nℤ (모듈러 산술)

    원소: {0, 1, 2, ..., n-1}
    연산: 모듈러 덧셈 (a + b mod n)
    항등원: 0
    역원: n - a (mod n)

    이것은 시계의 원리입니다!
    12시 다음은 1시 → ℤ/12ℤ
    """
    elements = list(range(n))
    op = lambda a, b: (a + b) % n
    inv = lambda a: (n - a) % n
    return Group(elements, op, 0, inv, name=f"ℤ/{n}ℤ")


def example_symmetric_group_3() -> Group:
    """
    예시: 정삼각형의 대칭군 S₃

    정삼각형을 자기 자신에 겹치게 만드는 변환(대칭)들의 모임:
        e  = 항등 (아무것도 안 함)
        r  = 120° 회전
        r² = 240° 회전
        s  = 반사 (축 1)
        sr = 반사 후 120° 회전
        sr²= 반사 후 240° 회전

    총 6개의 원소. 이것은 교환법칙이 성립하지 않는 군!
    (회전 후 반사 ≠ 반사 후 회전)
    """
    # 치환(permutation)으로 표현: (1,2,3)의 순열
    from itertools import permutations

    elements = list(permutations([1, 2, 3]))
    identity = (1, 2, 3)

    def compose(perm1, perm2):
        """치환의 합성: perm1 ∘ perm2"""
        return tuple(perm1[perm2[i]-1] for i in range(3))

    def inverse(perm):
        """치환의 역"""
        inv = [0, 0, 0]
        for i in range(3):
            inv[perm[i]-1] = i + 1
        return tuple(inv)

    return Group(elements, compose, identity, inverse, name="S₃")


# ============================================================================
#  환 (Ring)
# ============================================================================

class Ring:
    """
    환(Ring): 두 가지 연산을 가진 대수 구조.

    정의:
        집합 R과 두 이항연산 +, ×의 삼중 (R, +, ×)이 다음을 만족할 때:

        (R1) (R, +)는 아벨군  [덧셈에 대한 군 구조]
        (R2) 곱셈의 결합법칙: (a × b) × c = a × (b × c)
        (R3) 분배법칙:
             a × (b + c) = a × b + a × c  (좌분배)
             (a + b) × c = a × c + b × c  (우분배)

    우리가 이미 본 예시:
        - (ℤ, +, ×): 정수와 덧셈·곱셈. Phase 4에서 구성한 것!

    환에는 곱셈의 역원이 반드시 존재하지 않습니다:
        ℤ에서 2의 곱셈 역원 1/2는 ℤ에 없습니다.
        이것이 환과 체의 차이입니다.
    """

    def __init__(self, elements, add_op, mul_op, zero, one, add_inv, name="R"):
        self.elements = list(elements)
        self.add = add_op
        self.mul = mul_op
        self.zero = zero
        self.one = one
        self.add_inv = add_inv
        self.name = name

    def verify_ring_axioms(self) -> bool:
        """환 공리를 검증합니다."""
        E = self.elements

        # (R1) (R, +)는 아벨군
        print(f"  (R1) 덧셈 아벨군 검증:")
        add_group = Group(E, self.add, self.zero, self.add_inv, f"{self.name}_+")
        if not add_group.verify_axioms():
            return False
        if not add_group.is_abelian():
            print(f"  ✗ 덧셈 교환법칙 실패")
            return False
        print(f"  ✓ 덧셈 교환법칙")

        # (R2) 곱셈 결합법칙
        for a in E:
            for b in E:
                for c in E:
                    if self.mul(self.mul(a, b), c) != self.mul(a, self.mul(b, c)):
                        print(f"  ✗ 곱셈 결합법칙 실패")
                        return False
        print(f"  ✓ (R2) 곱셈 결합법칙")

        # (R3) 분배법칙
        for a in E:
            for b in E:
                for c in E:
                    left = self.mul(a, self.add(b, c))
                    right = self.add(self.mul(a, b), self.mul(a, c))
                    if left != right:
                        print(f"  ✗ 좌분배법칙 실패")
                        return False
        print(f"  ✓ (R3) 분배법칙")

        return True


# ============================================================================
#  체 (Field)
# ============================================================================

class Field(Ring):
    """
    체(Field): 사칙연산이 자유로운 대수 구조.

    정의:
        환 (F, +, ×)이 다음을 추가로 만족할 때:
        (F1) 곱셈의 교환법칙: a × b = b × a
        (F2) 곱셈의 항등원: ∃1 ∈ F, ∀a, 1 × a = a
        (F3) 곱셈의 역원: ∀a ≠ 0, ∃a⁻¹, a × a⁻¹ = 1

    즉: 체 = 환 + 곱셈 아벨군(0 제외)

    우리가 이미 본 예시:
        - (ℚ, +, ×): 유리수. Phase 5에서 구성한 것!
        - (ℝ, +, ×): 실수. Phase 6에서 구성한 것!

    체에서는 사칙연산이 자유롭습니다:
        a + b, a - b, a × b, a ÷ b (b ≠ 0) 모두 가능.
    """

    def __init__(self, elements, add_op, mul_op, zero, one, add_inv, mul_inv, name="F"):
        super().__init__(elements, add_op, mul_op, zero, one, add_inv, name)
        self.mul_inv = mul_inv

    def verify_field_axioms(self) -> bool:
        """체 공리를 검증합니다."""
        if not self.verify_ring_axioms():
            return False

        E = self.elements

        # 곱셈 교환법칙
        for a in E:
            for b in E:
                if self.mul(a, b) != self.mul(b, a):
                    print(f"  ✗ 곱셈 교환법칙 실패")
                    return False
        print(f"  ✓ 곱셈 교환법칙")

        # 곱셈 역원
        for a in E:
            if a != self.zero:
                a_inv = self.mul_inv(a)
                if self.mul(a, a_inv) != self.one:
                    print(f"  ✗ 곱셈 역원 실패: {a} × {a_inv} ≠ {self.one}")
                    return False
        print(f"  ✓ 곱셈 역원 (0 제외)")

        return True


def example_field_Z5() -> Field:
    """
    예시: ℤ/5ℤ — 5개 원소의 유한체

    원소: {0, 1, 2, 3, 4}
    연산: 모듈러 덧셈과 곱셈

    5가 소수이므로, 모든 0이 아닌 원소에 곱셈 역원이 존재합니다:
        1⁻¹ = 1 (1×1 = 1)
        2⁻¹ = 3 (2×3 = 6 ≡ 1)
        3⁻¹ = 2 (3×2 = 6 ≡ 1)
        4⁻¹ = 4 (4×4 = 16 ≡ 1)
    """
    n = 5
    elements = list(range(n))

    def mul_inv(a):
        for b in range(1, n):
            if (a * b) % n == 1:
                return b
        raise ValueError(f"{a}의 역원이 없음")

    return Field(
        elements,
        add_op=lambda a, b: (a + b) % n,
        mul_op=lambda a, b: (a * b) % n,
        zero=0, one=1,
        add_inv=lambda a: (n - a) % n,
        mul_inv=mul_inv,
        name="ℤ/5ℤ"
    )


# ============================================================================
#  구조 보존 사상 (Homomorphism)
# ============================================================================

def demonstrate_homomorphisms():
    """
    구조 보존 사상(homomorphism)을 설명합니다.

    Phase 2-6에서의 "매장(embedding)"이
    사실 대수적 구조를 보존하는 사상이었음을 보여줍니다:
        ℕ → ℤ: 환 준동형 (덧셈과 곱셈을 보존)
        ℤ → ℚ: 환 준동형
        ℚ → ℝ: 체 준동형
    """
    print("구조 보존 사상 (Homomorphism)")
    print("-" * 50)

    print("\n  Phase 2-6의 매장이 사실 대수적 구조를 보존하는 사상이었습니다:")
    print()
    print("    ℕ ──→ ℤ ──→ ℚ ──→ ℝ")
    print("    n ↦ (n,0)  z ↦ z/1  q ↦ 절단")
    print()
    print("  각 매장은:")
    print("    f(a + b) = f(a) + f(b)  [덧셈 보존]")
    print("    f(a × b) = f(a) × f(b)  [곱셈 보존]")
    print("    f(0) = 0, f(1) = 1      [항등원 보존]")
    print()
    print("  이것이 '구조 보존 사상' = 준동형(homomorphism)입니다.")
    print("  특히 단사(injective)이므로 '매장'(embedding)이라 합니다.")
    print()
    print("  💡 추상화의 위력:")
    print("  '준동형은 구조를 보존한다'는 것을 한 번 증명하면,")
    print("  모든 군, 환, 체에 적용됩니다!")


# ============================================================================
#  인터랙티브 데모
# ============================================================================

if __name__ == "__main__":
    print("╔══════════════════════════════════════════════════════════╗")
    print("║  Phase 7: 대수 구조 — 반복되는 패턴을 추상화하기      ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print()

    # 군 예시 1: ℤ/6ℤ
    print("예시 1: ℤ/6ℤ (시계 산술, 군)")
    print("=" * 50)
    Z6 = example_integers_mod_n(6)
    Z6.verify_axioms()
    print(f"  아벨군인가? {Z6.is_abelian()}")
    print(f"\n  케일리 표 (연산표):")
    Z6.cayley_table()

    # 군 예시 2: S₃
    print(f"\n\n예시 2: S₃ (정삼각형의 대칭군)")
    print("=" * 50)
    S3 = example_symmetric_group_3()
    S3.verify_axioms()
    print(f"  아벨군인가? {S3.is_abelian()}")
    print(f"  → 회전 후 반사 ≠ 반사 후 회전 (비가환군!)")

    # 환 예시
    print(f"\n\n환 (Ring): 덧셈 + 곱셈")
    print("=" * 50)
    print("  (ℤ, +, ×)는 환입니다 — Phase 4에서 구성한 것!")
    print("  · (ℤ, +)는 아벨군: 항등원 0, 역원 -n")
    print("  · 곱셈은 결합법칙, 분배법칙 만족")
    print("  · 하지만 곱셈의 역원이 항상 있지는 않음: 2의 역원 1/2 ∉ ℤ")

    # 체 예시: ℤ/5ℤ
    print(f"\n\n예시 3: ℤ/5ℤ (유한체)")
    print("=" * 50)
    Z5 = example_field_Z5()
    Z5.verify_field_axioms()
    print(f"\n  곱셈 역원:")
    for a in range(1, 5):
        print(f"    {a}⁻¹ = {Z5.mul_inv(a)}  ({a} × {Z5.mul_inv(a)} = {(a * Z5.mul_inv(a)) % 5})")

    print(f"\n  케일리 표 (곱셈):")
    print(f"  × | 1  2  3  4")
    print(f"  ──┼────────────")
    for a in range(1, 5):
        row = "  ".join(f"{(a*b)%5}" for b in range(1, 5))
        print(f"  {a} | {row}")

    # 체의 계보
    print(f"\n\n체(Field)의 계보")
    print("=" * 50)
    print("  (ℚ, +, ×) — 유리수 체  (Phase 5)")
    print("  (ℝ, +, ×) — 실수 체    (Phase 6)")
    print("  (ℤ/pℤ, +, ×) — 유한체  (p가 소수일 때)")
    print()
    print("  체에서는 사칙연산이 자유롭습니다:")
    print("  덧셈, 뺄셈, 곱셈, 나눗셈(0 제외) 모두 가능!")

    # 구조 보존 사상
    print()
    demonstrate_homomorphisms()

    # 메타 성찰
    print(f"\n\n메타 성찰")
    print("=" * 50)
    print("  추상화란 구체적 대상에서 패턴을 추출하여")
    print("  그 패턴 자체를 연구하는 것입니다.")
    print()
    print("  (ℤ, +), (ℚ\\{{0}}, ×), (S₃, ∘) — 구체적 대상은 다르지만")
    print("  '군'이라는 공통 구조를 가집니다.")
    print()
    print("  '항등원은 유일하다'를 군 수준에서 한 번 증명하면,")
    print("  이 모든 구체적 사례에 한꺼번에 적용됩니다.")
    print()
    print("  → Phase 8에서는 실수의 완비성을 활용하여 해석학을 시작합니다.")
