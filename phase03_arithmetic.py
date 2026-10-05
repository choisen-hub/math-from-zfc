"""
Phase 3: 자연수의 산술 — 덧셈과 곱셈을 정의하기
=================================================

Phase 2에서 자연수라는 대상을 만들었으니,
이제 그 위에서 연산을 정의할 차례입니다.

"1 + 1 = 2"라는 명제는 직관적으로 당연해 보이지만,
공리적 체계에서는 "덧셈이 무엇인지"를 먼저 정의해야 합니다.

핵심 도구는 **재귀적 정의**(recursive definition)입니다.

재귀적 정의의 정당화:
    "n + S(m) = S(n + m)"이라는 규칙이
    실제로 잘 정의된 함수를 만들어내는가?
    이것을 보장하는 것이 ZFC의 치환 공리꼴(Axiom Schema of Replacement)입니다.

    직관적으로: 재귀 규칙이 각 입력에 대해 유일한 출력을 결정하면,
    그 입출력 쌍의 모임이 함수가 됩니다.
    치환 공리꼴이 이 모임이 집합(따라서 함수)임을 보장합니다.
"""

from phase02_natural_numbers import NaturalNumber


# ============================================================================
#  덧셈의 재귀적 정의
# ============================================================================

def add(a: int, b: int, verbose: bool = False) -> int:
    """
    자연수의 덧셈을 재귀적으로 정의합니다.

    정의:
        n + 0    = n              (기저 조건: 0을 더하면 변하지 않는다)
        n + S(m) = S(n + m)       (재귀 단계: m의 후계자를 더하는 것은
                                   n + m의 후계자와 같다)

    왜 이렇게 정의하는가?
    --------------------
    "덧셈"이란 "후계자 함수를 반복 적용하는 것"입니다.
    n + 3 = S(S(S(n))) — n에서 출발하여 후계자를 3번 적용합니다.

    이 재귀적 정의가 ZFC 안에서 정당화되려면 치환 공리꼴이 필요합니다:
    재귀 규칙이 정의하는 함수의 그래프가 집합임을 보장합니다.

    예시:
        2 + 3을 계산해봅시다:
        2 + 3 = 2 + S(2)         (3 = S(2)이므로)
              = S(2 + 2)         (재귀 단계 적용)
              = S(2 + S(1))      (2 = S(1)이므로)
              = S(S(2 + 1))      (재귀 단계 적용)
              = S(S(2 + S(0)))   (1 = S(0)이므로)
              = S(S(S(2 + 0)))   (재귀 단계 적용)
              = S(S(S(2)))       (기저 조건 적용)
              = S(S(3))
              = S(4)
              = 5
    """
    steps = []

    def _add(n, m, depth=0):
        if m == 0:
            # 기저 조건: n + 0 = n
            if verbose:
                steps.append(f"{'  ' * depth}{n} + 0 = {n}  [기저: n + 0 = n]")
            return n
        else:
            # 재귀 단계: n + S(m-1) = S(n + (m-1))
            if verbose:
                steps.append(f"{'  ' * depth}{n} + {m} = {n} + S({m-1}) = S({n} + {m-1})")
            result = _add(n, m - 1, depth + 1) + 1  # S(n + (m-1))
            if verbose:
                steps.append(f"{'  ' * depth}= S({result - 1}) = {result}")
            return result

    result = _add(a, b)
    if verbose:
        print(f"\n  {a} + {b}의 재귀적 계산 과정:")
        for step in steps:
            print(f"    {step}")
        print(f"  결과: {a} + {b} = {result}")
    return result


# ============================================================================
#  곱셈의 재귀적 정의
# ============================================================================

def mul(a: int, b: int, verbose: bool = False) -> int:
    """
    자연수의 곱셈을 재귀적으로 정의합니다.

    정의:
        n × 0    = 0              (기저 조건: 0을 곱하면 0이다)
        n × S(m) = n × m + n      (재귀 단계: m의 후계자를 곱하는 것은
                                    n × m에 n을 한 번 더 더하는 것)

    왜 이렇게 정의하는가?
    --------------------
    "곱셈"이란 "덧셈을 반복하는 것"입니다.
    n × 3 = n + n + n — n을 3번 더합니다.

    Phase 3의 핵심 통찰:
        후계자 → 덧셈 → 곱셈
        (반복)   (반복)
        각 연산은 이전 연산의 "반복 적용"입니다.

    예시:
        2 × 3을 계산해봅시다:
        2 × 3 = 2 × S(2)         (3 = S(2)이므로)
              = 2 × 2 + 2        (재귀 단계)
              = (2 × S(1) + 2)   (2 = S(1))
              = (2 × 1 + 2) + 2  (재귀 단계)
              = (2 × S(0) + 2) + 2
              = (2 × 0 + 2 + 2) + 2
              = (0 + 2 + 2) + 2   (기저: 2 × 0 = 0)
              = 6
    """
    steps = []

    def _mul(n, m, depth=0):
        if m == 0:
            if verbose:
                steps.append(f"{'  ' * depth}{n} × 0 = 0  [기저: n × 0 = 0]")
            return 0
        else:
            if verbose:
                steps.append(f"{'  ' * depth}{n} × {m} = {n} × {m-1} + {n}")
            partial = _mul(n, m - 1, depth + 1)
            result = partial + n  # n × (m-1) + n (덧셈은 이미 정의됨)
            if verbose:
                steps.append(f"{'  ' * depth}= {partial} + {n} = {result}")
            return result

    result = _mul(a, b)
    if verbose:
        print(f"\n  {a} × {b}의 재귀적 계산 과정:")
        for step in steps:
            print(f"    {step}")
        print(f"  결과: {a} × {b} = {result}")
    return result


# ============================================================================
#  덧셈의 기본 성질 (귀납법으로 증명)
# ============================================================================

def demonstrate_addition_properties():
    """
    덧셈의 기본 성질을 구체적 예시로 검증하고,
    귀납법 증명의 구조를 보여줍니다.

    1. 교환법칙: n + m = m + n
    2. 결합법칙: (n + m) + k = n + (m + k)
    3. 항등원: n + 0 = 0 + n = n
    """
    print("=" * 60)
    print("덧셈의 기본 성질")
    print("=" * 60)

    # 교환법칙
    print("\n  1. 교환법칙: n + m = m + n")
    print("  " + "-" * 40)
    for n in range(5):
        for m in range(5):
            assert add(n, m) == add(m, n), f"교환법칙 위반: {n}+{m} ≠ {m}+{n}"
    print("  ✓ n, m ∈ {0,...,4} 에서 모두 검증됨")

    print("\n  교환법칙의 귀납 증명 구조:")
    print("  (1) 기저: n + 0 = 0 + n을 먼저 증명 (이것도 귀납법 필요!)")
    print("  (2) 보조정리: n + S(m) = S(n) + m")
    print("  (3) 귀납 단계: n + S(m) = S(n + m) = S(m + n) [귀납가정]")
    print("                         = m + S(n) [보조정리] = S(m) + n")

    # 결합법칙
    print("\n  2. 결합법칙: (n + m) + k = n + (m + k)")
    print("  " + "-" * 40)
    for n in range(4):
        for m in range(4):
            for k in range(4):
                assert add(add(n, m), k) == add(n, add(m, k))
    print("  ✓ n, m, k ∈ {0,...,3} 에서 모두 검증됨")

    print("\n  결합법칙의 귀납 증명 (k에 대한 귀납):")
    print("  기저: (n+m)+0 = n+m = n+(m+0)  ✓")
    print("  귀납: (n+m)+S(k) = S((n+m)+k)       [덧셈 정의]")
    print("                   = S(n+(m+k))       [귀납 가정]")
    print("                   = n+S(m+k)         [덧셈 정의]")
    print("                   = n+(m+S(k))       [덧셈 정의]  ✓")


def demonstrate_multiplication_properties():
    """
    곱셈의 기본 성질을 구체적 예시로 검증합니다.

    1. 교환법칙: n × m = m × n
    2. 결합법칙: (n × m) × k = n × (m × k)
    3. 분배법칙: n × (m + k) = n × m + n × k
    """
    print("\n" + "=" * 60)
    print("곱셈의 기본 성질")
    print("=" * 60)

    # 교환법칙
    print("\n  1. 교환법칙: n × m = m × n")
    for n in range(5):
        for m in range(5):
            assert mul(n, m) == mul(m, n)
    print("  ✓ n, m ∈ {0,...,4} 에서 모두 검증됨")

    # 결합법칙
    print("\n  2. 결합법칙: (n × m) × k = n × (m × k)")
    for n in range(4):
        for m in range(4):
            for k in range(4):
                assert mul(mul(n, m), k) == mul(n, mul(m, k))
    print("  ✓ n, m, k ∈ {0,...,3} 에서 모두 검증됨")

    # 분배법칙
    print("\n  3. 분배법칙: n × (m + k) = n × m + n × k")
    for n in range(4):
        for m in range(4):
            for k in range(4):
                assert mul(n, add(m, k)) == add(mul(n, m), mul(n, k))
    print("  ✓ n, m, k ∈ {0,...,3} 에서 모두 검증됨")

    print("\n  💡 분배법칙은 덧셈과 곱셈을 연결하는 다리입니다.")
    print("  이것이 Phase 7(대수 구조)에서 '환(ring)'의 핵심 조건이 됩니다.")


# ============================================================================
#  순서와 연산의 관계
# ============================================================================

def demonstrate_order_and_operations():
    """
    순서와 덧셈의 관계를 보여줍니다.

    핵심: n ≤ m ⟺ ∃k, n + k = m
    "m이 n보다 크거나 같다"는 것은 "n에 뭔가를 더해서 m을 만들 수 있다"는 것입니다.
    """
    print("\n" + "=" * 60)
    print("순서와 연산의 관계: n ≤ m ⟺ ∃k, n + k = m")
    print("=" * 60)

    for n in range(5):
        for m in range(n, 5):
            k = m - n
            print(f"  {n} ≤ {m}: {n} + {k} = {m}  ✓")


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
    print("║  Phase 3: 자연수의 산술 — 덧셈과 곱셈을 정의하기      ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print()

    # 덧셈의 재귀적 계산 과정
    print("덧셈의 재귀적 정의: n + 0 = n,  n + S(m) = S(n + m)")
    print("-" * 55)
    add(2, 3, verbose=True)
    add(0, 4, verbose=True)
    add(3, 0, verbose=True)

    # 곱셈의 재귀적 계산 과정
    print("\n\n곱셈의 재귀적 정의: n × 0 = 0,  n × S(m) = n × m + n")
    print("-" * 55)
    mul(2, 3, verbose=True)
    mul(3, 4, verbose=True)
    mul(0, 5, verbose=True)

    # 성질 검증
    demonstrate_addition_properties()
    demonstrate_multiplication_properties()
    demonstrate_order_and_operations()

    # 인터랙티브
    print("\n\n" + "=" * 60)
    print("인터랙티브 모드: 덧셈/곱셈의 재귀적 계산 과정")
    print("=" * 60)
    while True:
        try:
            user_input = _ask("\n두 자연수를 입력하세요 (예: 3 4, q: 종료): ").strip()
            if user_input.lower() == 'q':
                break
            parts = user_input.split()
            a, b = int(parts[0]), int(parts[1])
            if a < 0 or b < 0:
                print("자연수(0 이상)를 입력해주세요.")
                continue
            add(a, b, verbose=True)
            mul(a, b, verbose=True)
        except (ValueError, IndexError):
            print("예시: 3 4")
        except KeyboardInterrupt:
            break

    print("\n\n→ Phase 4에서는 '3 - 5'를 정의하기 위해 정수를 구성합니다.")
