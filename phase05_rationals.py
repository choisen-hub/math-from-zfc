"""
Phase 5: 유리수의 구성 — 나눗셈의 한계를 넘기
=============================================

정수에서 3 ÷ 2는 정의되지 않습니다.

Phase 4에서 뺄셈 문제를 해결한 것과 **정확히 같은 전략**을 씁니다:
    (a, b)라는 정수 쌍을 "a/b를 의미하는 것"으로 해석합니다.

구조적 유사성 (패턴의 반복!):
    ┌─────────────────────────────────────────────────────────┐
    │ 정수 구성:   (a,b) ~ (c,d) ⟺ a + d = b + c           │
    │              [덧셈으로 뺄셈을 우회]                     │
    │                                                         │
    │ 유리수 구성: (a,b) ~ (c,d) ⟺ a × d = b × c           │
    │              [곱셈으로 나눗셈을 우회]                   │
    └─────────────────────────────────────────────────────────┘
    같은 패턴이 반복됩니다!

유리수의 성질:
    유리수 ℚ는 사칙연산이 자유롭게 가능한 첫 번째 체계입니다.
    (0으로 나누는 것만 제외하면) 덧셈, 뺄셈, 곱셈, 나눗셈 모두 가능합니다.
    이런 구조를 "체(field)"라고 합니다 (Phase 7에서 자세히).

유리수의 한계:
    유리수는 조밀하지만 "구멍"이 있습니다.
    √2에 해당하는 유리수는 존재하지 않습니다!
    이것이 Phase 6(실수의 구성)의 동기가 됩니다.
"""

from phase04_integers import Integer


# ============================================================================
#  동치 관계
# ============================================================================

def rational_equiv(a1: int, b1: int, a2: int, b2: int) -> bool:
    """
    두 정수 쌍 (a1, b1)과 (a2, b2)가 같은 유리수를 나타내는지 판정합니다.

    동치 관계:
        (a1, b1) ~ (a2, b2) ⟺ a1 × b2 = b1 × a2

    이것은 a1/b1 = a2/b2를 나눗셈 없이 표현한 것입니다.

    예시:
        1. (1, 2) ~ (2, 4): 1×4 = 2×2? 4 = 4 ✓ (둘 다 1/2)
        2. (3, 6) ~ (1, 2): 3×2 = 6×1? 6 = 6 ✓ (둘 다 1/2)
        3. (-1, 3) ~ (1, -3): (-1)×(-3) = 3×1? 3 = 3 ✓ (둘 다 -1/3)
    """
    return a1 * b2 == b1 * a2


# ============================================================================
#  유리수 클래스
# ============================================================================

class Rational:
    """
    유리수 = 정수 쌍 (분자, 분모)의 동치류.

    내부 표현: 기약분수 (약분된 형태)
        (a, b) → (a/gcd, b/gcd) (b > 0이 되도록 부호 조정)

    연산:
        덧셈: (a,b) + (c,d) = (ad + bc, bd)
        뺄셈: (a,b) - (c,d) = (ad - bc, bd)
        곱셈: (a,b) × (c,d) = (ac, bd)
        나눗셈: (a,b) ÷ (c,d) = (ad, bc)  (c ≠ 0)

    체(field) 구조:
        유리수는 사칙연산이 자유롭게 가능한 첫 번째 체계입니다!
        (정수는 나눗셈이 안 되므로 체가 아닙니다.)
    """

    def __init__(self, numerator: int, denominator: int = 1):
        """유리수 numerator/denominator를 구성합니다."""
        if denominator == 0:
            raise ZeroDivisionError(
                "분모가 0인 유리수는 존재하지 않습니다. "
                "(a, 0)은 어떤 유리수도 나타내지 않습니다."
            )
        # 기약분수로 정규화
        from math import gcd
        g = gcd(abs(numerator), abs(denominator))
        # 분모를 양수로
        sign = 1 if denominator > 0 else -1
        self.num = sign * numerator // g
        self.den = sign * denominator // g

    def equivalence_class(self, max_show: int = 5) -> list:
        """이 유리수에 해당하는 동치류의 대표원들을 보여줍니다."""
        result = []
        for k in range(1, max_show + 1):
            result.append((self.num * k, self.den * k))
        return result

    def __add__(self, other: 'Rational') -> 'Rational':
        """
        유리수의 덧셈: (a/b) + (c/d) = (ad + bc) / bd

        Well-definedness:
            대표원이 달라도 결과가 같음을 보장합니다.
            분배법칙과 곱셈의 교환법칙으로 증명 가능합니다.
        """
        return Rational(self.num * other.den + other.num * self.den,
                        self.den * other.den)

    def __sub__(self, other: 'Rational') -> 'Rational':
        """유리수의 뺄셈: a/b - c/d = (ad - bc) / bd"""
        return Rational(self.num * other.den - other.num * self.den,
                        self.den * other.den)

    def __mul__(self, other: 'Rational') -> 'Rational':
        """유리수의 곱셈: (a/b) × (c/d) = ac / bd"""
        return Rational(self.num * other.num, self.den * other.den)

    def __truediv__(self, other: 'Rational') -> 'Rational':
        """
        유리수의 나눗셈: (a/b) ÷ (c/d) = ad / bc

        드디어! 나눗셈이 (0을 제외하고) 항상 가능합니다!
        유리수가 "체(field)"인 이유입니다.
        """
        if other.num == 0:
            raise ZeroDivisionError("0으로 나눌 수 없습니다.")
        return Rational(self.num * other.den, self.den * other.num)

    def __neg__(self) -> 'Rational':
        return Rational(-self.num, self.den)

    def __eq__(self, other):
        if isinstance(other, Rational):
            return self.num == other.num and self.den == other.den
        return NotImplemented

    def __lt__(self, other: 'Rational') -> bool:
        """순서: a/b < c/d ⟺ ad < bc (분모 양수 가정)"""
        return self.num * other.den < other.num * self.den

    def __le__(self, other: 'Rational') -> bool:
        return self == other or self < other

    def __float__(self):
        return self.num / self.den

    def __repr__(self):
        if self.den == 1:
            return f"Rational({self.num})"
        return f"Rational({self.num}, {self.den})"

    def __str__(self):
        if self.den == 1:
            return str(self.num)
        return f"{self.num}/{self.den}"

    def __hash__(self):
        return hash((self.num, self.den))


# ============================================================================
#  정수의 매장
# ============================================================================

def embed_integer_to_rational(z: int) -> Rational:
    """
    정수를 유리수로 매장합니다: n ↦ (n, 1) = n/1

    이 매장은 사칙연산을 보존합니다.
    "정수가 유리수 '안에' 살고 있다."
    """
    return Rational(z, 1)


# ============================================================================
#  유리수의 조밀성
# ============================================================================

def demonstrate_density():
    """
    유리수의 조밀성(density)을 보여줍니다.

    조밀성: 두 유리수 사이에 항상 또 다른 유리수가 있습니다.
    증명: a < b이면, (a + b) / 2도 유리수이고, a < (a+b)/2 < b
    """
    print("유리수의 조밀성: 두 유리수 사이에 항상 유리수가 있다")
    print("-" * 50)

    a, b = Rational(1, 3), Rational(1, 2)
    print(f"  {a}와 {b} 사이:")
    current_a, current_b = a, b
    for i in range(6):
        mid = (current_a + current_b) * Rational(1, 2)
        print(f"    중간점: {mid} = {float(mid):.10f}")
        current_a, current_b = current_a, mid

    print(f"\n  → 이 과정을 무한히 반복할 수 있습니다!")
    print(f"  → 유리수는 '빈틈없이 촘촘해 보입니다'")
    print(f"  → 하지만... 정말 빈틈이 없을까요?")


# ============================================================================
#  √2의 비합리성 증명
# ============================================================================

def prove_sqrt2_irrational():
    """
    √2가 유리수가 아님을 증명합니다 (귀류법).

    이것은 유리수의 "보이지 않는 구멍"의 존재를 보여줍니다.

    증명:
        √2 = a/b (a, b는 서로소인 정수)라고 가정하자.
        양변을 제곱하면: 2 = a²/b²
        따라서: a² = 2b²

        a²이 짝수이므로 a도 짝수 (a = 2k로 쓸 수 있다)
        (2k)² = 2b² → 4k² = 2b² → b² = 2k²
        b²이 짝수이므로 b도 짝수

        a와 b가 모두 짝수 → 서로소가 아님! 모순!
        따라서 √2는 유리수가 아니다. ∎

    역사적 맥락:
        기원전 5세기, 피타고라스 학파는 "모든 것은 수(유리수)의 비율"이라 믿었다.
        히파수스가 √2의 비합리성을 발견했을 때,
        이는 피타고라스 학파의 세계관을 뒤흔드는 사건이었다.
    """
    print("\n√2의 비합리성 증명 (귀류법)")
    print("-" * 50)
    print("  가정: √2 = a/b (a, b는 서로소)")
    print("  → a² = 2b²")
    print("  → a²은 짝수 → a는 짝수 → a = 2k")
    print("  → (2k)² = 2b² → 4k² = 2b² → b² = 2k²")
    print("  → b²은 짝수 → b도 짝수")
    print("  → a, b 모두 짝수 → 서로소가 아님! 모순! ∎")

    # √2 근방의 유리수들
    print(f"\n  √2 ≈ 1.41421356...")
    print(f"  √2 근방의 유리수들:")
    import math
    sqrt2 = math.sqrt(2)
    approximations = []
    for d in range(1, 20):
        n = round(sqrt2 * d)
        r = Rational(n, d)
        diff = abs(float(r) - sqrt2)
        approximations.append((r, diff))

    approximations.sort(key=lambda x: x[1])
    for r, diff in approximations[:8]:
        print(f"    {r} = {float(r):.10f}  (오차: {diff:.10f})")

    print(f"\n  → 유리수로 √2에 아무리 가까이 가도, 정확히 √2인 유리수는 없습니다!")
    print(f"  → 유리수에는 '보이지 않는 구멍'이 있습니다.")
    print(f"  → 이 구멍을 메우는 것이 Phase 6(실수의 구성)의 목표입니다.")


# ============================================================================
#  인터랙티브 데모
# ============================================================================

if __name__ == "__main__":
    print("╔══════════════════════════════════════════════════════════╗")
    print("║  Phase 5: 유리수의 구성 — 나눗셈의 한계를 넘기        ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print()

    # 구조적 유사성
    print("Phase 4와의 구조적 유사성")
    print("-" * 50)
    print("  정수:   (a,b) ~ (c,d) ⟺ a + d = b + c  [덧셈으로 뺄셈 우회]")
    print("  유리수: (a,b) ~ (c,d) ⟺ a × d = b × c  [곱셈으로 나눗셈 우회]")
    print("  → 같은 패턴이 반복됩니다!")
    print()

    # 동치류
    print("유리수의 동치류 표현")
    print("-" * 50)
    for num, den in [(1, 2), (2, 3), (-1, 4), (3, 1)]:
        r = Rational(num, den)
        eq_class = r.equivalence_class()
        eq_str = " ~ ".join(f"({a},{b})" for a, b in eq_class)
        print(f"  유리수 {r} = {eq_str} ~ ...")

    # 연산
    print(f"\n유리수의 사칙연산 — 드디어 자유롭다!")
    print("-" * 50)
    examples = [(Rational(1,2), Rational(1,3)),
                (Rational(2,3), Rational(3,4)),
                (Rational(-1,2), Rational(3,5))]
    for a, b in examples:
        print(f"  {a} + {b} = {a + b}")
        print(f"  {a} - {b} = {a - b}")
        print(f"  {a} × {b} = {a * b}")
        print(f"  {a} ÷ {b} = {a / b}")
        print()

    # 체 구조
    print("체(Field)의 구조:")
    print("  ✓ 덧셈: 교환, 결합, 항등원(0), 역원(-a)")
    print("  ✓ 곱셈: 교환, 결합, 항등원(1), 역원(1/a, a≠0)")
    print("  ✓ 분배법칙")
    print("  → 유리수는 사칙연산이 자유로운 첫 번째 체계!")
    print()

    # 조밀성
    demonstrate_density()

    # √2
    prove_sqrt2_irrational()

    # 인터랙티브
    print("\n\n" + "=" * 60)
    print("인터랙티브 모드: 유리수의 정수 쌍 표현")
    print("=" * 60)
    while True:
        try:
            user_input = input("\n유리수를 입력하세요 (예: 3/4, q: 종료): ").strip()
            if user_input.lower() == 'q':
                break
            if '/' in user_input:
                parts = user_input.split('/')
                r = Rational(int(parts[0]), int(parts[1]))
            else:
                r = Rational(int(user_input))
            eq_class = r.equivalence_class(8)
            eq_str = " ~ ".join(f"({a},{b})" for a, b in eq_class)
            print(f"\n  유리수 {r} = {eq_str} ~ ...")
            print(f"  십진수 근사: {float(r):.10f}")
        except (ValueError, ZeroDivisionError) as e:
            print(f"  오류: {e}")
        except KeyboardInterrupt:
            break

    print("\n\n→ Phase 6에서는 유리수의 '구멍'을 메우기 위해 실수를 구성합니다.")
