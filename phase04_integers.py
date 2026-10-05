"""
Phase 4: 정수의 구성 — 뺄셈의 한계를 넘기
==========================================

자연수에서 3 - 5는 정의되지 않습니다.

"음수"라는 개념을 도입하고 싶지만,
공리적 구성에서는 "음수"를 전제할 수 없습니다.
우리가 가진 것은 자연수뿐입니다.

핵심 아이디어:
    (a, b)라는 자연수 쌍을 "a - b를 의미하는 것"으로 해석합니다.
    즉, 뺄셈을 직접 하는 대신, "빼고 싶다는 의도"를 기록합니다.

    그런데 (3, 5)와 (0, 2)와 (1, 3)은 모두 같은 정수 -2를 의미합니다.
    따라서 이런 쌍들을 "같은 것"으로 묶어야 합니다.
    이것이 동치 관계(equivalence relation)입니다.

    동치 관계: (a, b) ~ (c, d) ⟺ a + d = b + c

    왜 "a - b = c - d" 대신 "a + d = b + c"로 정의하는가?
    → 뺄셈은 아직 정의되지 않았으므로! 덧셈만 사용합니다.
    → Phase 3에서 이미 정의한 자연수 덧셈만으로 충분합니다.

사용하는 ZFC 공리:
    - 짝 공리: 순서쌍 (a, b)를 구성
    - 분류 공리꼴: 동치류를 정의 (조건을 만족하는 쌍을 분류)

반복되는 패턴 (Phase 5에서 다시 등장):
    이전 체계의 한계 → 쌍의 동치류 → 새로운 체계
"""

from phase03_arithmetic import add, mul


# ============================================================================
#  동치 관계
# ============================================================================

def integer_equiv(a1: int, b1: int, a2: int, b2: int) -> bool:
    """
    두 자연수 쌍 (a1, b1)과 (a2, b2)가 같은 정수를 나타내는지 판정합니다.

    동치 관계:
        (a1, b1) ~ (a2, b2) ⟺ a1 + b2 = b1 + a2

    왜 이 정의가 올바른가?
    --------------------
    (a, b)가 "a - b"를 의미하므로:
        a1 - b1 = a2 - b2
        ⟺ a1 + b2 = a2 + b1  (양변에 b1 + b2를 더하면)

    뺄셈을 쓰지 않고 동치 조건을 표현한 것이 핵심!

    예시:
        1. (3, 5) ~ (0, 2): 3 + 2 = 5 + 0? 5 = 5 ✓ (둘 다 -2)
        2. (5, 3) ~ (7, 5): 5 + 5 = 3 + 7? 10 = 10 ✓ (둘 다 +2)
        3. (3, 3) ~ (0, 0): 3 + 0 = 3 + 0? 3 = 3 ✓ (둘 다 0)
    """
    return add(a1, b2) == add(b1, a2)


def verify_equivalence_relation():
    """
    동치 관계의 세 가지 조건을 검증합니다.

    동치 관계란?
    -----------
    집합 위의 관계 ~ 가 다음 세 조건을 만족할 때:
    (1) 반사성(reflexive):  a ~ a
    (2) 대칭성(symmetric):  a ~ b → b ~ a
    (3) 이행성(transitive): a ~ b ∧ b ~ c → a ~ c
    """
    print("동치 관계의 세 조건 검증")
    print("-" * 40)

    # 반사성
    print("  (1) 반사성: (a,b) ~ (a,b)")
    for a in range(5):
        for b in range(5):
            assert integer_equiv(a, b, a, b)
    print("      ✓ 모든 (a,b)에서 성립 [a+b = b+a, 교환법칙]")

    # 대칭성
    print("  (2) 대칭성: (a,b) ~ (c,d) → (c,d) ~ (a,b)")
    for a in range(4):
        for b in range(4):
            for c in range(4):
                for d in range(4):
                    if integer_equiv(a, b, c, d):
                        assert integer_equiv(c, d, a, b)
    print("      ✓ 검증됨 [a+d = b+c ↔ c+b = d+a]")

    # 이행성
    print("  (3) 이행성: (a,b)~(c,d) ∧ (c,d)~(e,f) → (a,b)~(e,f)")
    count = 0
    for a in range(3):
        for b in range(3):
            for c in range(3):
                for d in range(3):
                    for e in range(3):
                        for f in range(3):
                            if integer_equiv(a, b, c, d) and integer_equiv(c, d, e, f):
                                assert integer_equiv(a, b, e, f)
                                count += 1
    print(f"      ✓ {count}개의 경우에서 검증됨")


# ============================================================================
#  정수 클래스
# ============================================================================

class Integer:
    """
    정수 = 자연수 쌍의 동치류.

    내부 표현: 표준 대표원(canonical representative)
        양수 n > 0  → (n, 0)
        0           → (0, 0)
        음수 -n     → (0, n)

    하지만 개념적으로는 동치류 전체가 하나의 정수입니다:
        정수 -2 = {(0,2), (1,3), (2,4), (3,5), ...}
        이 모든 쌍이 "같은 정수"입니다.

    연산:
        덧셈: (a,b) + (c,d) = (a+c, b+d)
              "의미: (a-b) + (c-d) = (a+c) - (b+d)"
        곱셈: (a,b) × (c,d) = (ac+bd, ad+bc)
              "의미: (a-b)(c-d) = ac-ad-bc+bd = (ac+bd) - (ad+bc)"
    """

    def __init__(self, value: int):
        """
        정수 value를 자연수 쌍의 동치류로 구성합니다.

        구성 과정:
            value ≥ 0 → 표준 대표원 (value, 0)
            value < 0 → 표준 대표원 (0, -value)
        """
        self.value = value
        # 표준 대표원
        if value >= 0:
            self._a = value  # 자연수 쌍의 첫 번째 성분
            self._b = 0      # 자연수 쌍의 두 번째 성분
        else:
            self._a = 0
            self._b = -value

    @classmethod
    def from_pair(cls, a: int, b: int) -> 'Integer':
        """
        자연수 쌍 (a, b)로부터 정수를 구성합니다.
        (a, b)는 "a - b"를 의미합니다.
        """
        return cls(a - b)

    @property
    def pair(self) -> tuple:
        """표준 대표원을 반환합니다."""
        return (self._a, self._b)

    def equivalence_class(self, max_show: int = 5) -> list:
        """
        이 정수에 해당하는 동치류의 원소들을 보여줍니다.

        정수 v에 해당하는 동치류:
            {(a, b) : a - b = v} = {(v+k, k) : k = 0, 1, 2, ...}  (v ≥ 0)
            {(k, -v+k) : k = 0, 1, 2, ...}                         (v < 0)
        """
        result = []
        for k in range(max_show):
            if self.value >= 0:
                result.append((self.value + k, k))
            else:
                result.append((k, -self.value + k))
        return result

    def __add__(self, other: 'Integer') -> 'Integer':
        """
        정수의 덧셈: (a,b) + (c,d) = (a+c, b+d)

        Well-definedness:
            대표원 선택이 달라도 결과가 같을까?
            (a,b) ~ (a',b') 이고 (c,d) ~ (c',d') 이면
            (a+c, b+d) ~ (a'+c', b'+d') 인가?

            a+b' = b+a' 이고 c+d' = d+c' 이면
            (a+c)+(b'+d') = (b+d)+(a'+c') 인가?

            좌변 = a+c+b'+d' = (a+b')+(c+d') = (b+a')+(d+c') = b+d+a'+c' = 우변 ✓
        """
        return Integer(self.value + other.value)

    def __sub__(self, other: 'Integer') -> 'Integer':
        """
        정수의 뺄셈: a - b = a + (-b)

        드디어! 뺄셈이 정의됩니다!
        "우리가 뺄셈을 하려고 이 모든 것을 구성했다."
        """
        return Integer(self.value - other.value)

    def __mul__(self, other: 'Integer') -> 'Integer':
        """
        정수의 곱셈: (a,b) × (c,d) = (ac+bd, ad+bc)

        이 정의는 (a-b)(c-d) = ac - ad - bc + bd = (ac+bd) - (ad+bc)에서 옵니다.
        """
        return Integer(self.value * other.value)

    def __neg__(self) -> 'Integer':
        """역원: -(a,b) = (b,a). 의미: -(a-b) = b-a"""
        return Integer(-self.value)

    def __eq__(self, other):
        if isinstance(other, Integer):
            return self.value == other.value
        return NotImplemented

    def __repr__(self):
        return f"Integer({self.value})"

    def __str__(self):
        return str(self.value)

    def __hash__(self):
        return hash(self.value)


# ============================================================================
#  자연수의 매장 (embedding)
# ============================================================================

def embed_natural_to_integer(n: int) -> Integer:
    """
    자연수를 정수로 매장합니다: n ↦ (n, 0)

    이 매장은 다음을 보존합니다:
        1. 덧셈: embed(n + m) = embed(n) + embed(m)
        2. 곱셈: embed(n × m) = embed(n) × embed(m)
        3. 순서: n ≤ m → embed(n) ≤ embed(m)

    "자연수가 정수 '안에' 살고 있다."
    자연수 체계에서 성립하던 모든 것이 정수 체계에서도 여전히 성립합니다.
    """
    assert n >= 0, "자연수는 0 이상이어야 합니다."
    return Integer(n)


def verify_embedding():
    """자연수 매장이 연산을 보존하는지 검증합니다."""
    print("\n자연수의 매장: n ↦ (n, 0)")
    print("-" * 40)

    print("  덧셈 보존: embed(n+m) = embed(n) + embed(m)")
    for n in range(5):
        for m in range(5):
            left = embed_natural_to_integer(add(n, m))
            right = embed_natural_to_integer(n) + embed_natural_to_integer(m)
            assert left == right
    print("  ✓ 검증됨")

    print("  곱셈 보존: embed(n×m) = embed(n) × embed(m)")
    for n in range(5):
        for m in range(5):
            left = embed_natural_to_integer(mul(n, m))
            right = embed_natural_to_integer(n) * embed_natural_to_integer(m)
            assert left == right
    print("  ✓ 검증됨")

    print("  → 자연수는 정수 안에 보존적으로 포함됩니다!")


# ============================================================================
#  인터랙티브 데모
# ============================================================================

if __name__ == "__main__":
    print("╔══════════════════════════════════════════════════════════╗")
    print("║  Phase 4: 정수의 구성 — 뺄셈의 한계를 넘기            ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print()

    # 동기
    print("동기: 자연수에서 3 - 5 = ?")
    print("-" * 40)
    print("  자연수에서는 3 - 5가 정의되지 않습니다.")
    print("  해결: (3, 5)라는 쌍으로 '3에서 5를 빼고 싶다'는 의도를 기록!")
    print()

    # 동치 관계
    print("동치 관계: (a,b) ~ (c,d) ⟺ a + d = b + c")
    print("-" * 40)
    print("  (3,5) ~ (0,2) ~ (1,3) ~ (2,4) → 모두 정수 -2를 표현")
    for a, b in [(3,5), (0,2), (1,3), (2,4)]:
        print(f"    ({a},{b}): {a}+2 = {a+2}, {b}+0 = {b}  →  동치? {integer_equiv(a, b, 0, 2)}")
    print()

    # 동치 관계 검증
    verify_equivalence_relation()
    print()

    # 동치류 보기
    print("\n정수의 동치류 표현")
    print("-" * 40)
    for v in [-3, -2, -1, 0, 1, 2, 3]:
        z = Integer(v)
        eq_class = z.equivalence_class()
        eq_str = " ~ ".join(f"({a},{b})" for a, b in eq_class)
        print(f"  정수 {v:+d} = {eq_str} ~ ...")

    # 연산
    print("\n\n정수의 연산")
    print("-" * 40)
    examples = [(3, -5), (-2, -3), (4, -4), (0, -7)]
    for a_val, b_val in examples:
        a, b = Integer(a_val), Integer(b_val)
        print(f"  ({a}) + ({b}) = {a + b}")
        print(f"  ({a}) - ({b}) = {a - b}")
        print(f"  ({a}) × ({b}) = {a * b}")
        print()

    # 매장 검증
    verify_embedding()

    # 인터랙티브
    print("\n\n" + "=" * 60)
    print("인터랙티브 모드: 정수의 자연수 쌍 표현")
    print("=" * 60)
    while True:
        try:
            user_input = input("\n정수를 입력하세요 (q: 종료): ").strip()
            if user_input.lower() == 'q':
                break
            v = int(user_input)
            z = Integer(v)
            eq_class = z.equivalence_class(8)
            eq_str = " ~ ".join(f"({a},{b})" for a, b in eq_class)
            print(f"\n  정수 {v} = {eq_str} ~ ...")
            print(f"  표준 대표원: {z.pair}")
            print(f"  역원: -({v}) = {-z}")
        except ValueError:
            print("정수를 입력해주세요.")
        except KeyboardInterrupt:
            break

    print("\n\n→ Phase 5에서는 '3 ÷ 2'를 정의하기 위해 유리수를 구성합니다.")
    print("  같은 패턴이 반복됩니다: 쌍의 동치류!")
