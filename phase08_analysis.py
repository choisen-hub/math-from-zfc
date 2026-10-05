"""
Phase 8: 기초 해석학 — 극한과 연속성
======================================

실수를 구성한 진짜 이유는 **해석학**을 하기 위해서입니다.

해석학의 핵심 개념은 "극한"이고,
극한이 제대로 작동하려면 실수의 완비성이 필수적입니다.

역사적 배경:
    뉴턴(Newton)과 라이프니츠(Leibniz)는 17세기에 미적분을 발명했습니다.
    하지만 "무한소"(infinitesimal)라는 모호한 개념에 의존했고,
    버클리 주교는 이를 "사라진 양의 유령"이라 비판했습니다.

    200년 후, 코시(Cauchy)와 바이어슈트라스(Weierstrass)가
    ε-δ 정의로 극한을 엄밀화했습니다.
    이 엄밀화의 토대가 바로 실수의 완비성입니다.

의존 관계:
    실수의 완비성 (Phase 6) → 극한의 존재 → 연속성 → 미분
"""

import math


# ============================================================================
#  수열과 극한
# ============================================================================

class Sequence:
    """
    수열: 자연수에서 실수로의 함수.

    수열 {aₙ}은 a₁, a₂, a₃, ... 의 무한한 나열입니다.
    수학적으로는 함수 a: ℕ → ℝ, n ↦ aₙ 입니다.
    """

    def __init__(self, formula, name: str = "aₙ"):
        """
        formula: n을 받아 aₙ을 반환하는 함수
        name: 수열의 이름 (표시용)
        """
        self.formula = formula
        self.name = name

    def term(self, n: int) -> float:
        """n번째 항 aₙ을 계산합니다."""
        return self.formula(n)

    def terms(self, start: int = 1, count: int = 10) -> list:
        """수열의 처음 몇 항을 반환합니다."""
        return [(n, self.term(n)) for n in range(start, start + count)]


def check_convergence(seq: Sequence, L: float, epsilon: float,
                       max_n: int = 100000) -> int:
    """
    수열이 L로 수렴하는지 검증하고, 주어진 ε에 대한 N을 찾습니다.

    극한의 ε-N 정의:
        lim(n→∞) aₙ = L
        ⟺ ∀ε > 0, ∃N ∈ ℕ, ∀n > N: |aₙ - L| < ε

    비형식적 해설:
        "아무리 작은 오차 범위(ε)를 잡아도,
         어느 시점(N) 이후로는 수열이 그 범위 안에 들어온다."

    이 함수는 주어진 ε에 대해 적절한 N을 찾아 반환합니다.
    N을 찾지 못하면 -1을 반환합니다.
    """
    for N in range(1, max_n):
        # N 이후의 모든 항이 ε-밴드 안에 있는지 확인
        # (유한하게 검사할 수밖에 없으므로, N+1부터 N+100까지 확인)
        all_inside = True
        for n in range(N + 1, N + 101):
            if abs(seq.term(n) - L) >= epsilon:
                all_inside = False
                break
        if all_inside:
            return N
    return -1


def demonstrate_limits():
    """
    극한의 개념과 ε-N 정의를 구체적 예시로 보여줍니다.
    """
    print("수열의 극한: ε-N 정의")
    print("=" * 55)

    print("""
  정의: lim(n→∞) aₙ = L
  ⟺ ∀ε > 0, ∃N ∈ ℕ, ∀n > N: |aₙ - L| < ε

  비형식적:
  "아무리 작은 오차 범위(ε)를 잡아도,
   어느 시점(N) 이후로는 수열이 그 범위 안에 들어온다."
""")

    # 예시 1: aₙ = 1/n → 0
    seq1 = Sequence(lambda n: 1/n, "1/n")
    print(f"  예시 1: aₙ = 1/n → 0")
    print(f"  처음 몇 항: {', '.join(f'{v:.4f}' for _, v in seq1.terms(1, 8))}")

    epsilons = [0.1, 0.01, 0.001, 0.0001]
    for eps in epsilons:
        N = check_convergence(seq1, 0, eps)
        print(f"    ε = {eps}: N = {N} (n > {N}이면 |1/n - 0| < {eps})")

    # 예시 2: aₙ = (n+1)/n → 1
    seq2 = Sequence(lambda n: (n+1)/n, "(n+1)/n")
    print(f"\n  예시 2: aₙ = (n+1)/n → 1")
    print(f"  처음 몇 항: {', '.join(f'{v:.4f}' for _, v in seq2.terms(1, 8))}")

    for eps in [0.1, 0.01, 0.001]:
        N = check_convergence(seq2, 1, eps)
        print(f"    ε = {eps}: N = {N}")

    # 예시 3: 발산하는 수열
    seq3 = Sequence(lambda n: (-1)**n, "(-1)ⁿ")
    print(f"\n  예시 3: aₙ = (-1)ⁿ (발산)")
    print(f"  처음 몇 항: {', '.join(f'{v:.0f}' for _, v in seq3.terms(1, 8))}")
    print(f"  → 1과 -1 사이를 왔다갔다 — 어떤 값에도 수렴하지 않음!")


# ============================================================================
#  극한의 기본 정리
# ============================================================================

def demonstrate_limit_theorems():
    """
    극한의 기본 정리들을 보여줍니다.

    1. 수렴 수열은 유계이다
    2. 극한의 사칙연산
    3. 단조수렴정리 (완비성이 핵심!)
    """
    print("\n극한의 기본 정리")
    print("=" * 55)

    # 1. 수렴 수열은 유계
    print("\n  정리 1: 수렴 수열은 유계이다")
    print("  aₙ = 1/n이 수렴 → {1, 1/2, 1/3, ...}는 유계 (0 ≤ aₙ ≤ 1)")
    print("  대우: 유계가 아닌 수열 (예: aₙ = n)은 발산한다")

    # 2. 극한의 사칙연산
    print("\n  정리 2: 극한의 사칙연산")
    print("  lim aₙ = A, lim bₙ = B이면:")
    print("    lim (aₙ + bₙ) = A + B")
    print("    lim (aₙ × bₙ) = A × B")
    print("    lim (aₙ / bₙ) = A / B  (B ≠ 0)")

    a = Sequence(lambda n: 1 + 1/n, "1+1/n")  # → 1
    b = Sequence(lambda n: 2 - 1/n, "2-1/n")  # → 2
    print(f"\n  예시: aₙ = 1+1/n → 1, bₙ = 2-1/n → 2")
    print(f"  aₙ + bₙ = {a.term(100) + b.term(100):.6f} → 3 ✓")
    print(f"  aₙ × bₙ = {a.term(100) * b.term(100):.6f} → 2 ✓")

    # 3. 단조수렴정리
    print("\n  정리 3: 단조수렴정리 ⭐")
    print("  단조증가이고 위로 유계인 수열은 수렴한다.")
    print()
    print("  ⚠ 이 정리에서 완비성이 사용됩니다!")
    print("  유리수에서는 이 정리가 성립하지 않습니다:")
    print()
    print("  반례: aₙ = √2의 n자리 소수점 근사 (유리수)")
    print("    a₁ = 1.4, a₂ = 1.41, a₃ = 1.414, ...")
    print("    단조증가 ✓, 위로 유계 (< 1.5) ✓")
    print("    하지만 극한 √2 ∉ ℚ!")
    print("    → 유리수에서는 극한이 '구멍'으로 빠져나갑니다.")
    print("    → 실수에서는 완비성 덕분에 이런 일이 없습니다!")


# ============================================================================
#  함수의 연속성
# ============================================================================

def demonstrate_continuity():
    """
    함수의 연속성을 ε-δ 정의로 설명합니다.

    정의:
        f가 x = a에서 연속이다
        ⟺ ∀ε > 0, ∃δ > 0, ∀x: |x - a| < δ → |f(x) - f(a)| < ε

    비형식적:
        "입력을 아주 조금만 바꾸면, 출력도 아주 조금만 바뀐다."
        "함수의 그래프를 연필을 떼지 않고 그릴 수 있다."
    """
    print("\n함수의 연속성: ε-δ 정의")
    print("=" * 55)

    print("""
  정의: f가 x = a에서 연속
  ⟺ ∀ε > 0, ∃δ > 0, ∀x: |x - a| < δ → |f(x) - f(a)| < ε

  비형식적:
  "입력을 조금 바꾸면, 출력도 조금만 바뀐다."
""")

    # 예시 1: f(x) = x² (연속)
    print("  예시 1: f(x) = x² (a = 2에서)")
    a = 2.0
    fa = a ** 2

    for eps in [0.1, 0.01, 0.001]:
        # f(x) = x², f(a) = 4
        # |x² - 4| < ε ← |x-2||x+2| < ε
        # |x-2| < 3이면 |x+2| < 5이므로, δ = ε/5면 충분
        delta = eps / 5
        print(f"    ε = {eps}: δ = {delta:.4f}")
        # 검증
        test_points = [a - delta/2, a + delta/2, a - delta*0.99, a + delta*0.99]
        all_ok = all(abs(x**2 - fa) < eps for x in test_points)
        print(f"      |x - {a}| < {delta:.4f}이면 |x² - {fa}| < {eps}? {all_ok} ✓")

    # 예시 2: 불연속 함수
    print(f"\n  예시 2: 불연속 함수")
    print(f"    f(x) = {{ 0  (x < 0)")
    print(f"           {{ 1  (x ≥ 0)")
    print(f"    x = 0에서 불연속:")
    print(f"    ε = 0.5를 잡으면, 어떤 δ > 0에 대해서도")
    print(f"    x = -δ/2에서 |f(x) - f(0)| = |0 - 1| = 1 > 0.5")
    print(f"    → δ를 아무리 작게 잡아도 ε-조건을 만족시킬 수 없다!")


# ============================================================================
#  미분
# ============================================================================

def demonstrate_derivative():
    """
    미분의 정의와 구체적 계산을 보여줍니다.

    정의:
        f'(x) = lim(h→0) [f(x+h) - f(x)] / h

    이 정의는 극한의 정의에 의존합니다.
    극한은 실수의 완비성에 의존합니다.
    완비성은 ZFC의 멱집합 공리에 의존합니다.

    의존 사슬:
        ZFC 공리 → 실수 → 극한 → 미분
    """
    print("\n미분: 극한으로 정의되는 순간 변화율")
    print("=" * 55)

    print("""
  정의: f'(x) = lim(h→0) [f(x+h) - f(x)] / h

  이것은 "함수의 순간 변화율"입니다.
  기하학적으로는 접선의 기울기입니다.
""")

    # 예시: (x²)' = 2x를 정의로부터 계산
    print("  예시: f(x) = x², f'(x) = ?")
    print()
    print("  f'(x) = lim(h→0) [(x+h)² - x²] / h")
    print("        = lim(h→0) [x² + 2xh + h² - x²] / h")
    print("        = lim(h→0) [2xh + h²] / h")
    print("        = lim(h→0) (2x + h)")
    print("        = 2x")
    print()
    print("  ∴ (x²)' = 2x  ✓")

    # 수치적 검증
    print("\n  수치적 검증: x = 3에서 f'(3) = 6")
    x = 3.0
    for h in [0.1, 0.01, 0.001, 0.0001, 0.00001]:
        approx = ((x + h)**2 - x**2) / h
        print(f"    h = {h}: [(3+h)² - 9] / h = {approx:.8f}  (오차: {abs(approx - 6):.2e})")

    print(f"\n  → h가 0에 가까워질수록, 차분 몫이 6에 수렴합니다.")
    print(f"  → 이것이 극한의 정의가 보장하는 것입니다.")

    # 의존 사슬
    print(f"\n  의존 사슬:")
    print(f"  ZFC 공리 → 집합 → 자연수 → 정수 → 유리수 → 실수(완비)")
    print(f"                                                ↓")
    print(f"                                              극한")
    print(f"                                                ↓")
    print(f"                                          연속성, 미분")
    print(f"\n  f'(x) = 2x라는 간단한 결과 뒤에")
    print(f"  ZFC로부터 시작된 긴 구성의 사슬이 있습니다!")


# ============================================================================
#  ε-밴드 시각화
# ============================================================================

def visualize_epsilon_band(seq_formula, L, name, epsilons=None):
    """
    수열의 수렴을 ε-밴드로 시각화합니다.
    (텍스트 기반 시각화)
    """
    if epsilons is None:
        epsilons = [0.5, 0.2, 0.1]

    print(f"\n  수열 aₙ = {name}, 극한 L = {L}")
    print(f"  {'n':>4} | {'aₙ':>10} | {'|aₙ-L|':>10} | ε-밴드 상태")
    print(f"  {'─'*4}─┼─{'─'*10}─┼─{'─'*10}─┼─{'─'*20}")

    min_eps = min(epsilons)
    for n in list(range(1, 12)) + [20, 50, 100]:
        an = seq_formula(n)
        diff = abs(an - L)
        status = ""
        for eps in sorted(epsilons, reverse=True):
            if diff < eps:
                status += f"[ε={eps}✓]"
        if not status:
            status = "밖"
        print(f"  {n:4d} | {an:10.6f} | {diff:10.6f} | {status}")


# ============================================================================
#  인터랙티브 데모
# ============================================================================


def _ask(prompt):
    """표준 입력이 터미널이 아니면(파이프·CI·에디터 실행) 대화형 모드를 건너뛴다."""
    import sys
    if not sys.stdin.isatty():
        print(prompt + "(비대화형 실행이라 건너뜀)")
        return "q"
    try:
        return input(prompt)
    except EOFError:
        return "q"


if __name__ == "__main__":
    print("╔══════════════════════════════════════════════════════════╗")
    print("║  Phase 8: 기초 해석학 — 극한과 연속성                  ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print()

    # 극한
    demonstrate_limits()

    # ε-밴드 시각화
    print(f"\n\nε-밴드 시각화")
    print("=" * 55)
    visualize_epsilon_band(lambda n: 1/n, 0, "1/n")
    visualize_epsilon_band(lambda n: (n+1)/n, 1, "(n+1)/n")

    # 극한의 정리
    demonstrate_limit_theorems()

    # 연속성
    demonstrate_continuity()

    # 미분
    demonstrate_derivative()

    # 인터랙티브: ε에 대한 N 찾기
    print(f"\n\n" + "=" * 55)
    print("인터랙티브 모드: ε를 입력하면 N을 찾아줍니다")
    print("수열: aₙ = 1/n, 극한 L = 0")
    print("=" * 55)

    while True:
        try:
            user_input = _ask("\nε을 입력하세요 (예: 0.01, q: 종료): ").strip()
            if user_input.lower() == 'q':
                break
            eps = float(user_input)
            if eps <= 0:
                print("ε은 양수여야 합니다!")
                continue
            seq = Sequence(lambda n: 1/n, "1/n")
            N = check_convergence(seq, 0, eps)
            if N > 0:
                print(f"\n  ε = {eps}에 대해 N = {N}")
                print(f"  n > {N}이면 |1/n - 0| = 1/n < {eps}")
                print(f"  확인: 1/{N+1} = {1/(N+1):.10f} < {eps}? {1/(N+1) < eps}")
            else:
                print(f"  N을 찾지 못했습니다.")
        except ValueError:
            print("양수를 입력해주세요.")
        except KeyboardInterrupt:
            break

    print("\n\n→ Phase 9에서는 전체를 조감합니다.")
