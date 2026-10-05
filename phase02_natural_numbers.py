"""
Phase 2: 자연수의 구성 — 무(無)에서 수를 만들기
================================================

자연수는 직관적으로 당연한 것처럼 느껴집니다.
1, 2, 3, ... — 손가락을 꼽으며 배우는 가장 기본적인 수학적 대상입니다.

하지만 ZFC에서는 자연수의 존재를 증명 없이 전제하지 않습니다.
"수"라는 것은 집합으로부터 **구성**되어야 합니다.

놀랍게도, '아무것도 없음'(공집합)으로부터 모든 자연수를 만들 수 있습니다!

폰 노이만 구성 (von Neumann construction)
-----------------------------------------
존 폰 노이만(John von Neumann)이 제안한 자연수의 집합론적 구성:

    0 = ∅ = {}                           (공집합 — 아무것도 없음)
    1 = {∅} = {0}                        (공집합을 담은 집합)
    2 = {∅, {∅}} = {0, 1}               (0과 1을 담은 집합)
    3 = {∅, {∅}, {∅, {∅}}} = {0, 1, 2}  (0, 1, 2를 담은 집합)
    ...
    n+1 = n ∪ {n}                        (후계자 함수)

핵심 관찰:
- 각 자연수 n은 집합이며, 그 원소는 정확히 {0, 1, ..., n-1}입니다.
- 즉, 각 자연수는 "자기보다 작은 모든 자연수의 모임"입니다.
- 집합 자체가 자신의 "크기"를 인코딩합니다: |n| = n

사용하는 ZFC 공리:
- 공집합 공리: 0 = ∅의 존재
- 짝 공리: {n}을 만들기 위해
- 합집합 공리: n ∪ {n}을 만들기 위해
- 무한 공리: {0, 1, 2, 3, ...} 전체가 집합으로 존재
"""

from phase01_zfc_axioms import AxiomOfPairing  # 순서쌍 구성에 사용


# ============================================================================
#  폰 노이만 서수 (Von Neumann Ordinal)
# ============================================================================

class VonNeumannOrdinal:
    """
    폰 노이만 서수로 표현된 자연수.

    각 자연수 n은 집합으로 표현됩니다:
        n = {0, 1, 2, ..., n-1}

    여기서 0, 1, 2, ... 각각도 집합입니다:
        0 = ∅ = frozenset()
        1 = {∅} = frozenset({frozenset()})
        2 = {∅, {∅}} = frozenset({frozenset(), frozenset({frozenset()})})

    내부적으로 실제 집합 표현(frozenset)을 유지하여,
    폰 노이만 구성이 실제로 작동하는 것을 확인할 수 있습니다.
    """

    # 캐시: 이미 구성한 서수를 저장
    _cache = {}

    def __init__(self, n: int):
        """
        자연수 n에 대응하는 폰 노이만 서수를 구성합니다.

        구성 과정:
            0 → ∅
            1 → {∅} = S(0)
            2 → {∅, {∅}} = S(1)
            ...
            n → S(n-1) = (n-1) ∪ {n-1}

        이 과정에서 사용되는 ZFC 공리:
            - 공집합 공리: 0 = ∅의 존재를 보장
            - 짝 공리: {n}을 구성하기 위해
            - 합집합 공리: n ∪ {n}을 계산하기 위해
        """
        if n < 0:
            raise ValueError(
                f"자연수는 0 이상이어야 합니다. "
                f"음수 {n}은 Phase 4(정수의 구성)에서 다룹니다."
            )
        self.n = n
        self._ordinal = self._build(n)

    @classmethod
    def _build(cls, n: int) -> frozenset:
        """
        n에 대응하는 폰 노이만 서수(집합)를 재귀적으로 구성합니다.

        이 재귀는 다음 공리들의 시뮬레이션입니다:
            기저: 0 = ∅  (공집합 공리)
            재귀: S(k) = k ∪ {k}  (짝 공리 + 합집합 공리)
        """
        if n in cls._cache:
            return cls._cache[n]

        if n == 0:
            # 공집합 공리: ∅이 존재한다
            result = frozenset()
        else:
            # 먼저 n-1을 구성한다
            prev = cls._build(n - 1)
            # 짝 공리로 {n-1}을 만든다
            singleton = frozenset({prev})
            # 합집합 공리로 (n-1) ∪ {n-1}을 만든다
            result = prev | singleton

        cls._cache[n] = result
        return result

    @property
    def as_set(self) -> frozenset:
        """폰 노이만 서수의 실제 집합 표현을 반환합니다."""
        return self._ordinal

    @property
    def elements_count(self) -> int:
        """
        이 서수의 원소 개수를 반환합니다.

        핵심: |n| = n — 자연수 n의 집합 표현은 정확히 n개의 원소를 가집니다!
        이것이 폰 노이만 구성의 우아함입니다.
        """
        return len(self._ordinal)

    def successor(self) -> 'VonNeumannOrdinal':
        """
        후계자 함수: S(n) = n ∪ {n}

        "다음 자연수"를 만듭니다.
        모든 자연수(0 제외)는 어떤 자연수의 후계자입니다:
            1 = S(0), 2 = S(1), 3 = S(2), ...
        """
        return VonNeumannOrdinal(self.n + 1)

    def show_construction(self) -> str:
        """
        이 자연수가 어떤 집합인지를 보기 좋게 표현합니다.

        예:
            3 → "3 = {∅, {∅}, {∅, {∅}}}"
            즉, "3 = {0, 1, 2}"
        """
        def set_to_str(s):
            if len(s) == 0:
                return "∅"
            elements = sorted(s, key=lambda x: len(str(x)))
            return "{" + ", ".join(set_to_str(e) for e in elements) + "}"

        formal = set_to_str(self._ordinal)
        informal = "{" + ", ".join(str(i) for i in range(self.n)) + "}" if self.n > 0 else "∅"
        return f"{self.n} = {formal}\n   즉, {self.n} = {informal}"

    def __eq__(self, other):
        """외연 공리: 같은 원소를 가지면 같다."""
        if isinstance(other, VonNeumannOrdinal):
            return self._ordinal == other._ordinal
        return NotImplemented

    def __lt__(self, other):
        """
        순서 관계: n < m ⟺ n ∈ m

        폰 노이만 구성의 놀라운 성질:
        원소 관계(∈)가 곧 엄격 순서(<)입니다!
        """
        if isinstance(other, VonNeumannOrdinal):
            return self._ordinal in other._ordinal
        return NotImplemented

    def __le__(self, other):
        """
        순서 관계: n ≤ m ⟺ n ⊆ m

        폰 노이만 구성의 또 다른 놀라운 성질:
        부분집합 관계(⊆)가 곧 순서(≤)입니다!
        """
        if isinstance(other, VonNeumannOrdinal):
            return self._ordinal <= other._ordinal  # frozenset의 <=는 ⊆
        return NotImplemented

    def __repr__(self):
        return f"VonNeumannOrdinal({self.n})"

    def __str__(self):
        return str(self.n)

    def __hash__(self):
        return hash(self.n)


# ============================================================================
#  자연수 클래스 (사용자 인터페이스)
# ============================================================================

class NaturalNumber(VonNeumannOrdinal):
    """
    자연수를 나타내는 클래스.

    내부적으로 폰 노이만 서수로 표현되며,
    Phase 3에서 정의할 덧셈과 곱셈의 토대가 됩니다.

    수학적 의미:
        자연수의 집합 ℕ = {0, 1, 2, 3, ...}은
        무한 공리에 의해 존재가 보장됩니다.

        각 원소는 폰 노이만 구성에 의해:
            n = {0, 1, 2, ..., n-1}
        으로 표현됩니다.
    """
    pass


# ============================================================================
#  순서 관계의 시뮬레이션
# ============================================================================

def demonstrate_order():
    """
    폰 노이만 구성에서 순서 관계가 자연스럽게 나타나는 것을 보여줍니다.

    핵심:
        n < m ⟺ n ∈ m  (원소 관계 = 엄격 순서)
        n ≤ m ⟺ n ⊆ m  (부분집합 관계 = 순서)
    """
    print("=" * 60)
    print("순서 관계: 원소 관계가 곧 순서이다!")
    print("=" * 60)

    nums = [NaturalNumber(i) for i in range(5)]

    print("\n  n ∈ m (원소 관계) = n < m (엄격 순서):")
    for i in range(4):
        for j in range(i+1, 5):
            in_relation = nums[i].as_set in nums[j].as_set
            print(f"    {i} ∈ {j}? {in_relation}  (즉, {i} < {j})")

    print("\n  n ⊆ m (부분집합 관계) = n ≤ m (순서):")
    for i in range(4):
        for j in range(i, 5):
            subset_relation = nums[i].as_set <= nums[j].as_set
            print(f"    {i} ⊆ {j}? {subset_relation}  (즉, {i} ≤ {j})")

    print("\n  💡 이것이 폰 노이만 구성의 우아함:")
    print("  별도의 '순서' 개념을 정의할 필요 없이,")
    print("  집합의 원소/부분집합 관계가 그대로 자연수의 순서가 됩니다!")


# ============================================================================
#  수학적 귀납법
# ============================================================================

def demonstrate_induction():
    """
    수학적 귀납법의 원리와 구체적 예시를 보여줍니다.

    수학적 귀납법은 무한 공리와 분류 공리꼴로부터 도출됩니다:

    원리:
        P(0)이 참이고,
        모든 n에 대해 P(n) → P(S(n))이면,
        모든 자연수 n에 대해 P(n)이 참이다.

    ZFC에서의 정당화:
        S = {n ∈ ℕ : P(n)} (분류 공리꼴로 존재)
        P(0) → 0 ∈ S
        P(n) → P(S(n)) → S는 후계자에 닫힘
        따라서 S = ℕ (무한 공리에 의한 ℕ의 최소성)
    """
    print("=" * 60)
    print("수학적 귀납법: 무한 공리 + 분류 공리꼴의 결과")
    print("=" * 60)

    print("\n  원리:")
    print("  (1) P(0)이 참이다  [기저 단계]")
    print("  (2) 모든 n에 대해 P(n) → P(n+1)  [귀납 단계]")
    print("  ────────────────────────────────")
    print("  ∴ 모든 자연수 n에 대해 P(n)이 참이다")

    # 구체적 예시: 0 + 1 + 2 + ... + n = n(n+1)/2
    print("\n  예시: 0 + 1 + 2 + ... + n = n(n+1)/2")
    print()
    print("  기저 단계 (n=0):")
    print("    좌변 = 0")
    print("    우변 = 0·1/2 = 0")
    print("    ✓ 성립!")

    print("\n  귀납 단계:")
    print("    P(k)가 참이라 가정: 0+1+...+k = k(k+1)/2")
    print("    P(k+1)을 보이자: 0+1+...+k+(k+1)")
    print("      = k(k+1)/2 + (k+1)        (귀납 가정 사용)")
    print("      = (k+1)(k/2 + 1)")
    print("      = (k+1)(k+2)/2")
    print("    ✓ P(k+1) 성립!")

    # 구체적 검증
    print("\n  구체적 검증:")
    for n in range(8):
        left = sum(range(n + 1))
        right = n * (n + 1) // 2
        print(f"    n={n}: 0+1+...+{n} = {left},  n(n+1)/2 = {right}  {'✓' if left == right else '✗'}")


# ============================================================================
#  인터랙티브 데모
# ============================================================================

if __name__ == "__main__":
    print("╔══════════════════════════════════════════════════════════╗")
    print("║  Phase 2: 자연수의 구성 — 무(無)에서 수를 만들기       ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print()

    # 기본 구성 보여주기
    print("폰 노이만 구성: 공집합에서 자연수를 만들기")
    print("-" * 50)
    for i in range(6):
        nat = NaturalNumber(i)
        print(f"  {nat.show_construction()}")
        print(f"   원소 수: |{i}| = {nat.elements_count}  (집합 자체가 크기를 인코딩!)")
        print()

    # 후계자 함수
    print("후계자 함수: S(n) = n ∪ {n}")
    print("-" * 50)
    for i in range(5):
        nat = NaturalNumber(i)
        succ = nat.successor()
        print(f"  S({i}) = {i} ∪ {{{i}}} = {succ.n}")
    print()

    # 순서 관계
    demonstrate_order()
    print()

    # 귀납법
    demonstrate_induction()
    print()

    # 인터랙티브
    print("\n" + "=" * 60)
    print("인터랙티브 모드: 자연수의 폰 노이만 서수 표현")
    print("=" * 60)
    while True:
        try:
            user_input = input("\n자연수를 입력하세요 (q: 종료): ").strip()
            if user_input.lower() == 'q':
                break
            n = int(user_input)
            if n < 0:
                print("음수는 Phase 4에서 다룹니다!")
                continue
            if n > 10:
                print(f"(n={n}의 집합 표현은 매우 길어집니다. 처음 몇 줄만 보여드립니다.)")

            nat = NaturalNumber(n)
            print(f"\n  {nat.show_construction()}")
            print(f"  {n}의 원소는 {', '.join(str(i) for i in range(n))}이며,")
            print(f"  이것은 {n}보다 작은 모든 자연수입니다.")
            print(f"  |{n}| = {nat.elements_count}  (원소 수 = 자기 자신)")
        except ValueError:
            print("자연수(0 이상의 정수)를 입력해주세요.")
        except KeyboardInterrupt:
            break

    print("\n\n메타 성찰:")
    print("=" * 60)
    print("  우리는 방금 ZFC의 공리 4개(공집합, 짝, 합집합, 무한)만으로")
    print("  자연수 전체를 구성했습니다.")
    print("  라이프니츠가 꿈꿨던 '무에서 수를 만들기'가")
    print("  실제로 작동하는 것입니다.")
    print()
    print("  → Phase 3에서는 이 자연수 위에 덧셈과 곱셈을 정의합니다.")
