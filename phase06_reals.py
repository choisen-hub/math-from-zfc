"""
Phase 6: 실수의 구성 — 유리수의 구멍을 메우기
=============================================

유리수는 조밀(dense)하지만 "구멍"이 있습니다.
√2가 있어야 할 자리에 유리수가 없습니다.

실수는 이 구멍을 전부 메운 체계입니다.

구성 방법: 데데킨트 절단 (Dedekind Cut)
--------------------------------------
리하르트 데데킨트(Richard Dedekind)의 아이디어:

    "유리수 전체를 두 부분으로 자르는 방법이 곧 실수이다."

    절단(cut) = 유리수 전체를 두 집합 (L, R)로 나누는 것
    조건:
        1. L ∪ R = ℚ, L ∩ R = ∅  (유리수 전체를 빠짐없이 나눔)
        2. L의 모든 원소 < R의 모든 원소  (L이 왼쪽, R이 오른쪽)
        3. L에 최대원소가 없음  (핵심 조건!)

    직관: 유리수 직선을 가위로 자른다고 상상하세요.
    자르는 "위치"가 바로 실수입니다.

    - 유리수 3/2에서 자르면: L = {q : q < 3/2}, R = {q : q ≥ 3/2}
      → R에 최소원소(3/2)가 있음. 이것은 유리수에 해당하는 절단.

    - √2 위치에서 자르면: L = {q : q < 0 또는 q² < 2}, R = {q : q > 0 이고 q² ≥ 2}
      → R에 최소원소가 없음! 이것이 무리수에 해당하는 절단.

사용하는 ZFC 공리:
    - 분류 공리꼴: 유리수에서 조건을 만족하는 것들을 분류 (L, R 구성)
    - 멱집합 공리: 유리수의 부분집합이 존재 (절단 자체가 유리수의 부분집합)

전체 여정:
    ∅ → ℕ → ℤ → ℚ → ℝ
    공집합 → 자연수 → 정수 → 유리수 → 실수
    각 단계에서 이전 체계의 한계가 동기를 제공하고,
    ZFC의 집합 구성 능력이 도구를 제공했습니다.
"""

from phase05_rationals import Rational
import math


# ============================================================================
#  데데킨트 절단 (Dedekind Cut)
# ============================================================================

class DedekindCut:
    """
    데데킨트 절단으로 표현된 실수.

    절단 = (L, R)
        L: 유리수의 부분집합 (하부 집합, lower set)
        R: 유리수의 부분집합 (상부 집합, upper set)

    조건:
        1. L ∪ R = ℚ (빠짐없이 나눔)
        2. ∀p ∈ L, ∀q ∈ R: p < q (L이 왼쪽)
        3. L에 최대원소 없음

    이 프로그램에서의 구현:
        무한 집합을 직접 저장할 수 없으므로,
        L의 원소인지 판정하는 함수(predicate)로 표현합니다.
        이것은 ZFC에서 분류 공리꼴을 사용하는 것에 대응합니다:
        L = {q ∈ ℚ : predicate(q)}
    """

    def __init__(self, predicate, name: str = "?", approx: float = None):
        """
        데데킨트 절단을 구성합니다.

        predicate: 유리수 q가 L에 속하는지 판정하는 함수
            predicate(num, den) -> bool
            (num/den이 L에 속하면 True)
        name: 이 절단이 나타내는 실수의 이름
        approx: 십진수 근사값 (시각화용)
        """
        self._predicate = predicate
        self.name = name
        self.approx = approx

    def is_in_lower(self, num: int, den: int) -> bool:
        """유리수 num/den이 하부 집합 L에 속하는지 판정합니다."""
        return self._predicate(num, den)

    def show_cut(self, sample_range: int = 20, denominator: int = 10):
        """
        절단의 모습을 유한한 유리수 표본으로 시각화합니다.

        L에 속하는 유리수와 R에 속하는 유리수를 분류하여 보여줍니다.
        """
        L_samples = []
        R_samples = []

        for num in range(-sample_range, sample_range + 1):
            if self.is_in_lower(num, denominator):
                L_samples.append(f"{num}/{denominator}")
            else:
                R_samples.append(f"{num}/{denominator}")

        print(f"  실수 {self.name}의 데데킨트 절단 (분모={denominator} 표본):")
        if len(L_samples) > 8:
            print(f"    L = {{..., {', '.join(L_samples[-5:])}}}")
        else:
            print(f"    L = {{{', '.join(L_samples)}}}")
        if len(R_samples) > 8:
            print(f"    R = {{{', '.join(R_samples[:5])}, ...}}")
        else:
            print(f"    R = {{{', '.join(R_samples)}}}")
        if self.approx is not None:
            print(f"    절단 위치 ≈ {self.approx}")


# ============================================================================
#  구체적 실수의 데데킨트 절단
# ============================================================================

def cut_rational(p: int, q: int) -> DedekindCut:
    """
    유리수 p/q에 해당하는 데데킨트 절단을 구성합니다.

    L = {r ∈ ℚ : r < p/q}
    R = {r ∈ ℚ : r ≥ p/q}

    R에 최소원소 p/q가 있습니다.
    이것이 "유리수에 해당하는 절단"의 특징입니다.
    """
    def predicate(num, den):
        # num/den < p/q ⟺ num*q < p*den (den, q > 0 가정)
        if den > 0 and q > 0:
            return num * q < p * den
        elif den < 0 and q > 0:
            return num * q > p * den
        elif den > 0 and q < 0:
            return num * q > p * den
        else:
            return num * q < p * den

    return DedekindCut(predicate, f"{p}/{q}" if q != 1 else str(p),
                       approx=p/q)


def cut_sqrt2() -> DedekindCut:
    """
    √2에 해당하는 데데킨트 절단을 구성합니다.

    L = {q ∈ ℚ : q < 0 또는 q² < 2}
    R = {q ∈ ℚ : q ≥ 0 이고 q² ≥ 2}

    핵심: R에 최소원소가 없습니다!
    왜? q² = 2인 유리수 q가 존재하지 않으므로 (Phase 5에서 증명).
    R의 어떤 원소 r에 대해서도, r² > 2이므로,
    r보다 작지만 여전히 제곱이 2 이상인 유리수가 존재합니다.
    """
    def predicate(num, den):
        # q = num/den
        # q < 0 또는 q² < 2
        if den == 0:
            return False
        q_sign = (num > 0 and den > 0) or (num < 0 and den < 0)
        if not q_sign and num != 0:
            return True  # q < 0
        if num == 0:
            return True  # 0 < √2
        # q > 0: q² < 2 ⟺ num² < 2·den²
        return num * num < 2 * den * den

    return DedekindCut(predicate, "√2", approx=math.sqrt(2))


def cut_pi() -> DedekindCut:
    """π에 해당하는 데데킨트 절단 (근사)."""
    def predicate(num, den):
        if den == 0:
            return False
        return num / den < math.pi

    return DedekindCut(predicate, "π", approx=math.pi)


# ============================================================================
#  실수의 완비성 (상한 성질)
# ============================================================================

def demonstrate_completeness():
    """
    실수의 완비성(completeness)을 보여줍니다.

    상한 성질 (Least Upper Bound Property):
        위로 유계인 비어있지 않은 실수 집합은 상한(supremum)을 가진다.

    이것이 유리수에서는 성립하지 않음:
        S = {q ∈ ℚ : q² < 2} — 위로 유계이지만 상한이 ℚ에 없음!
        상한은 √2이지만, √2 ∉ ℚ.

    실수에서는:
        S = {x ∈ ℝ : x² < 2} — 상한은 √2 ∈ ℝ. ✓

    이것이 해석학 전체의 토대입니다:
        극한의 존재, 중간값 정리, 볼차노-바이어슈트라스 정리 등
        모두 완비성에 의존합니다. (Phase 8에서 자세히)
    """
    print("실수의 완비성: 상한 성질")
    print("-" * 50)

    print("\n  유리수에서의 실패:")
    print("  S = {q ∈ ℚ : q² < 2}")
    print("  S의 원소 예시:")
    approx = []
    for d in range(1, 15):
        for n in range(1, d * 2):
            if n * n < 2 * d * d:
                approx.append((n, d))
    # 가장 큰 것들만 보여주기
    approx.sort(key=lambda x: x[0]/x[1], reverse=True)
    for n, d in approx[:5]:
        r = Rational(n, d)
        print(f"    {r} = {float(r):.6f}  (({r})² = {float(r)**2:.6f} < 2 ✓)")

    print(f"\n  이 집합의 상한은 √2 ≈ {math.sqrt(2):.10f}")
    print(f"  하지만 √2 ∉ ℚ! 유리수에서는 상한이 존재하지 않습니다.")
    print(f"\n  실수에서는:")
    print(f"  √2 ∈ ℝ (데데킨트 절단으로 구성됨)")
    print(f"  → 상한이 존재합니다. 완비성 성립! ✓")
    print(f"\n  💡 이것이 유리수와 실수의 결정적 차이이며,")
    print(f"  해석학(극한, 연속, 미분)이 가능한 이유입니다.")


# ============================================================================
#  칸토어의 대각선 논증
# ============================================================================

def demonstrate_diagonal_argument():
    """
    칸토어의 대각선 논증: 실수는 자연수와 일대일 대응이 불가능합니다.

    즉, |ℕ| < |ℝ| — 실수가 자연수보다 "더 많습니다".
    무한에도 크기가 다른 단계가 있습니다!

    증명 (귀류법):
        [0, 1) 구간의 실수를 모두 나열할 수 있다고 가정:
            r₁ = 0.d₁₁ d₁₂ d₁₃ d₁₄ ...
            r₂ = 0.d₂₁ d₂₂ d₂₃ d₂₄ ...
            r₃ = 0.d₃₁ d₃₂ d₃₃ d₃₄ ...
            ...

        대각선으로 새 수를 만든다:
            x = 0.e₁ e₂ e₃ ...
            여기서 eₙ ≠ dₙₙ (대각선의 각 자리와 다른 수를 선택)

        그러면 x ≠ rₙ (모든 n에 대해, n번째 자리가 다르므로)
        x는 목록에 없다! 모순!

    멱집합 공리와의 연결:
        칸토어는 |A| < |P(A)|를 증명했습니다.
        이 논증은 본질적으로 같은 아이디어입니다.
    """
    print("\n칸토어의 대각선 논증: 실수는 셀 수 없다")
    print("-" * 50)

    import random
    random.seed(42)

    # 시뮬레이션: "나열"을 시도
    print("\n  [0, 1)의 실수를 나열하려 시도합니다:")
    n_rows = 6
    digits_per_row = 10
    matrix = []
    for i in range(n_rows):
        row = [random.randint(0, 9) for _ in range(digits_per_row)]
        matrix.append(row)
        digits_str = ''.join(map(str, row))
        # 대각선 자리 강조
        highlighted = ""
        for j, d in enumerate(row):
            if j == i:
                highlighted += f"[{d}]"
            else:
                highlighted += f" {d} "
        print(f"    r{i+1} = 0.{highlighted} ...")

    # 대각선에서 새 수 구성
    diagonal = [matrix[i][i] for i in range(n_rows)]
    new_digits = [(d + 1) % 10 for d in diagonal]  # 각 자리를 다르게

    print(f"\n  대각선: {'  '.join(f'[{d}]' for d in diagonal)}")
    print(f"  새 수:  {'  '.join(f'[{d}]' for d in new_digits)}")
    new_str = ''.join(map(str, new_digits))
    print(f"  x = 0.{new_str}...")

    print(f"\n  x ≠ r1 (1번째 자리가 다름: {new_digits[0]} ≠ {diagonal[0]})")
    print(f"  x ≠ r2 (2번째 자리가 다름: {new_digits[1]} ≠ {diagonal[1]})")
    print(f"  x ≠ r3 (3번째 자리가 다름: {new_digits[2]} ≠ {diagonal[2]})")
    print(f"  ... 모든 rₙ과 다름!")

    print(f"\n  → x는 목록에 없다! 어떤 나열도 불완전하다.")
    print(f"  → 실수는 자연수와 일대일 대응 불가능 (비가산 무한)")
    print(f"  → |ℕ| < |ℝ| : 무한에도 크기가 다른 단계가 있다!")

    print(f"\n  📝 연속체 가설:")
    print(f"  |ℕ|과 |ℝ| 사이에 다른 크기의 무한이 있는가?")
    print(f"  괴델(1940)과 코헨(1963)이 증명한 것:")
    print(f"  이 질문은 ZFC로는 답할 수 없다! (독립 명제)")
    print(f"  → ZFC에도 한계가 있다는 깊은 사실입니다.")


# ============================================================================
#  인터랙티브 데모
# ============================================================================

if __name__ == "__main__":
    print("╔══════════════════════════════════════════════════════════╗")
    print("║  Phase 6: 실수의 구성 — 유리수의 구멍을 메우기        ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print()

    # 데데킨트 절단 예시
    print("데데킨트 절단: 유리수를 '두 부분으로 자르기'")
    print("=" * 55)

    # 유리수 3/2의 절단
    cut_3_2 = cut_rational(3, 2)
    cut_3_2.show_cut(denominator=4)
    print(f"    → R에 최소원소 3/2가 있음 (유리수에 해당하는 절단)")
    print()

    # √2의 절단
    cut_s2 = cut_sqrt2()
    cut_s2.show_cut(denominator=10)
    print(f"    → R에 최소원소가 없음! (무리수에 해당하는 절단)")
    print()

    # √2 근방의 유리수들 시각화
    print("\n√2 근방의 L/R 경계:")
    print("-" * 50)
    sqrt2 = math.sqrt(2)
    for d in [10, 100, 1000]:
        n_below = int(sqrt2 * d)
        n_above = n_below + 1
        r_below = Rational(n_below, d)
        r_above = Rational(n_above, d)
        print(f"  분모 {d:4d}: L ∋ {r_below} = {float(r_below):.6f}"
              f"  |  {r_above} = {float(r_above):.6f} ∈ R")
    print(f"  {'':>14}√2 ≈ {sqrt2:.6f} (이 사이의 '구멍')")

    # 유리수 매장
    print(f"\n\n유리수의 매장: q ↦ 절단 ({{r : r < q}}, {{r : r ≥ q}})")
    print("-" * 50)
    print("  유리수 q는 자연스럽게 실수(데데킨트 절단)로 매장됩니다.")
    print("  N ⊂ Z ⊂ Q ⊂ R — 수 체계가 계속 확장됩니다!")

    # 완비성
    print()
    demonstrate_completeness()

    # 대각선 논증
    print()
    demonstrate_diagonal_argument()

    # 전체 여정 회고
    print("\n\n" + "=" * 60)
    print("전체 여정 회고")
    print("=" * 60)
    print("""
  ∅ → ℕ → ℤ → ℚ → ℝ

  각 단계에서:
  - 이전 체계의 한계가 동기를 제공했다:
    · ℕ: 뺄셈 불가 → ℤ
    · ℤ: 나눗셈 불가 → ℚ
    · ℚ: 구멍 존재 → ℝ

  - ZFC의 집합 구성 능력이 도구를 제공했다:
    · 공집합 → 자연수 (공집합, 짝, 합집합, 무한 공리)
    · 쌍의 동치류 → 정수, 유리수 (분류 공리꼴)
    · 부분집합 (절단) → 실수 (멱집합, 분류 공리꼴)

  - 동치류라는 같은 패턴이 반복되었다:
    · ℤ = ℕ² / ~ (덧셈으로 우회)
    · ℚ = ℤ² / ~ (곱셈으로 우회)
    · ℝ = P(ℚ)의 특별한 부분집합 (데데킨트 절단)
""")

    print("→ Phase 7에서는 이 반복되는 패턴을 추상화합니다 (군, 환, 체).")
    print("→ Phase 8에서는 실수의 완비성을 활용하여 해석학을 시작합니다.")
