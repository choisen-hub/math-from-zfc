"""
의존 관계 시각화 유틸리티
========================

이 모듈은 math-from-zfc 프로젝트의 개념적 의존 관계를
그래프로 시각화합니다.

"어떤 개념이 어떤 개념 위에 쌓여 있는지"를 한눈에 보여줌으로써,
수학이라는 건물의 구조를 이해하는 데 도움을 줍니다.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.font_manager as fm

# macOS 한글 폰트 설정
for font_name in ['AppleGothic', 'Apple SD Gothic Neo', 'NanumGothic', 'Malgun Gothic']:
    font_list = fm.findSystemFonts()
    if any(font_name.lower().replace(' ', '') in f.lower().replace(' ', '') for f in font_list):
        plt.rcParams['font.family'] = font_name
        break
plt.rcParams['axes.unicode_minus'] = False
import json
import os


# ── 의존 관계 데이터 ──────────────────────────────────────────────
# 각 노드: (id, 이름, Phase, 사용된 ZFC 공리)
# 각 간선: (출발, 도착, "왜 이 의존이 필요한가")

NODES = [
    ("zfc",      "ZFC 공리계",        1, []),
    ("empty",    "공집합 ∅",         1, ["공집합 공리"]),
    ("pair",     "짝 공리",          1, ["짝 공리"]),
    ("union",    "합집합 공리",       1, ["합집합 공리"]),
    ("infinity",  "무한 공리",        1, ["무한 공리"]),
    ("separation","분류 공리꼴",      1, ["분류 공리꼴"]),
    ("powerset",  "멱집합 공리",      1, ["멱집합 공리"]),
    ("replacement","치환 공리꼴",     1, ["치환 공리꼴"]),
    ("nat",      "자연수 ℕ",         2, ["공집합", "짝", "합집합", "무한"]),
    ("add",      "덧셈",             3, ["치환 공리꼴"]),
    ("mul",      "곱셈",             3, ["치환 공리꼴"]),
    ("int",      "정수 ℤ",           4, ["분류 공리꼴"]),
    ("rat",      "유리수 ℚ",         5, ["분류 공리꼴"]),
    ("real",     "실수 ℝ",           6, ["분류 공리꼴", "멱집합 공리"]),
    ("group",    "군 (Group)",       7, []),
    ("ring",     "환 (Ring)",        7, []),
    ("field",    "체 (Field)",       7, []),
    ("limit",    "극한",             8, []),
    ("cont",     "연속성",           8, []),
    ("deriv",    "미분",             8, []),
]

EDGES = [
    ("zfc",   "empty",    "공집합의 존재를 보장"),
    ("zfc",   "pair",     "두 집합의 짝을 보장"),
    ("zfc",   "union",    "합집합의 존재를 보장"),
    ("zfc",   "infinity", "무한 집합의 존재를 보장"),
    ("zfc",   "separation","조건부 부분집합 추출"),
    ("zfc",   "powerset", "멱집합의 존재를 보장"),
    ("zfc",   "replacement","함수 이미지가 집합임을 보장"),
    ("empty", "nat",      "0 = ∅에서 출발"),
    ("pair",  "nat",      "후계자 S(n) = n ∪ {n} 구성"),
    ("union", "nat",      "후계자 구성에 합집합 필요"),
    ("infinity","nat",    "자연수 전체가 집합으로 존재"),
    ("nat",   "add",      "자연수 위에 덧셈을 정의"),
    ("nat",   "mul",      "자연수 위에 곱셈을 정의"),
    ("add",   "int",      "덧셈으로 동치관계 정의: a+d=b+c"),
    ("mul",   "int",      "곱셈 연산의 well-definedness"),
    ("int",   "rat",      "정수 쌍으로 유리수 구성"),
    ("rat",   "real",     "유리수의 구멍을 데데킨트 절단으로 메움"),
    ("nat",   "group",    "(ℤ,+)가 군의 예시"),
    ("int",   "group",    "(ℤ,+)가 군의 예시"),
    ("int",   "ring",     "(ℤ,+,×)가 환의 예시"),
    ("rat",   "field",    "(ℚ,+,×)가 체의 예시"),
    ("real",  "field",    "(ℝ,+,×)가 체의 예시"),
    ("real",  "limit",    "실수의 완비성이 극한 보장"),
    ("limit", "cont",     "연속성은 극한으로 정의"),
    ("cont",  "deriv",    "미분은 극한으로 정의"),
]


# Phase별 색상
PHASE_COLORS = {
    1: "#FFB3BA",  # 분홍 - ZFC 공리
    2: "#FFDFBA",  # 주황 - 자연수
    3: "#FFFFBA",  # 노랑 - 산술
    4: "#BAFFC9",  # 초록 - 정수
    5: "#BAE1FF",  # 파랑 - 유리수
    6: "#D4BAFF",  # 보라 - 실수
    7: "#FFD4E5",  # 핑크 - 대수 구조
    8: "#D4F0F0",  # 청록 - 해석학
}


def build_dependency_data():
    """의존 관계 데이터를 딕셔너리로 구조화합니다."""
    nodes_dict = {}
    for nid, name, phase, axioms in NODES:
        nodes_dict[nid] = {
            "name": name,
            "phase": phase,
            "axioms": axioms,
        }

    edges_list = []
    for src, dst, reason in EDGES:
        edges_list.append({
            "from": src,
            "to": dst,
            "reason": reason,
        })

    return {"nodes": nodes_dict, "edges": edges_list}


def visualize_dependency_graph(save_path=None):
    """
    의존 관계 그래프를 matplotlib로 시각화합니다.

    각 노드에는 개념 이름이, 각 간선에는 "왜 이 의존이 필요한지"가
    라벨로 표시됩니다.
    """
    fig, ax = plt.subplots(1, 1, figsize=(18, 22))
    ax.set_xlim(-1, 11)
    ax.set_ylim(-1, 24)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title("math-from-zfc: 개념 의존 관계 그래프",
                 fontsize=16, fontweight='bold', pad=20)

    # 노드 위치 (수동 레이아웃)
    positions = {
        "zfc":     (5, 23),
        "empty":   (1, 20), "pair":    (3, 20), "union":    (5, 20),
        "infinity":(7, 20), "separation":(9, 20),
        "powerset":(2, 18), "replacement":(8, 18),
        "nat":     (5, 15),
        "add":     (3.5, 12), "mul": (6.5, 12),
        "int":     (5, 9),
        "rat":     (5, 6),
        "real":    (5, 3),
        "group":   (1, 6), "ring": (1, 4), "field": (1, 2),
        "limit":   (8, 3),
        "cont":    (8, 1),
        "deriv":   (10, 1),
    }

    # 간선 그리기
    for src, dst, reason in EDGES:
        if src in positions and dst in positions:
            x1, y1 = positions[src]
            x2, y2 = positions[dst]
            ax.annotate(
                "", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", color="#888888",
                                lw=1.0, connectionstyle="arc3,rad=0.1"),
            )

    # 노드 그리기
    for nid, name, phase, axioms in NODES:
        if nid not in positions:
            continue
        x, y = positions[nid]
        color = PHASE_COLORS.get(phase, "#DDDDDD")
        bbox = dict(boxstyle="round,pad=0.4", facecolor=color,
                    edgecolor="#333333", linewidth=1.5)
        ax.text(x, y, name, ha='center', va='center',
                fontsize=9, fontweight='bold', bbox=bbox)

    # 범례
    legend_patches = []
    phase_names = {
        1: "Phase 1: ZFC 공리",
        2: "Phase 2: 자연수",
        3: "Phase 3: 산술",
        4: "Phase 4: 정수",
        5: "Phase 5: 유리수",
        6: "Phase 6: 실수",
        7: "Phase 7: 대수 구조",
        8: "Phase 8: 해석학",
    }
    for phase_num in sorted(PHASE_COLORS):
        legend_patches.append(
            mpatches.Patch(color=PHASE_COLORS[phase_num],
                           label=phase_names.get(phase_num, f"Phase {phase_num}"))
        )
    ax.legend(handles=legend_patches, loc='lower left', fontsize=8)

    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"그래프가 {save_path}에 저장되었습니다.")
    else:
        plt.show()
    plt.close(fig)


def print_dependency_table():
    """ZFC 공리 사용 추적표를 텍스트로 출력합니다."""
    print("=" * 65)
    print("ZFC 공리 사용 추적표")
    print("=" * 65)

    axiom_usage = {
        "공집합 공리":   "0의 존재 (Phase 2)",
        "짝 공리":      "후계자 구성, 순서쌍 (Phase 2, 4, 5)",
        "합집합 공리":   "후계자 구성 (Phase 2)",
        "무한 공리":     "자연수 전체의 존재 (Phase 2)",
        "분류 공리꼴":   "동치류, 데데킨트 절단 (Phase 4, 5, 6)",
        "멱집합 공리":   "실수의 존재, 대각선 논증 (Phase 6)",
        "치환 공리꼴":   "재귀적 정의의 정당화 (Phase 3)",
        "선택 공리":     "(이 프로그램에서는 명시적으로 불필요)",
        "외연 공리":     "집합의 동일성 판정 (전체)",
        "정칙성 공리":   "집합의 자기포함 방지 (배경 가정)",
    }

    for axiom, usage in axiom_usage.items():
        print(f"  {axiom:<12}  →  {usage}")
    print("=" * 65)


if __name__ == "__main__":
    print("math-from-zfc 의존 관계 시각화")
    print("-" * 40)

    print_dependency_table()
    print()

    out_path = os.path.join(os.path.dirname(__file__), "..", "dependency_graph.png")
    out_path = os.path.abspath(out_path)
    visualize_dependency_graph(save_path=out_path)

    print("\nJSON 형태 의존 관계 데이터:")
    data = build_dependency_data()
    print(json.dumps(data, ensure_ascii=False, indent=2)[:500] + "...")
