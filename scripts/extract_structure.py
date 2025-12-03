#!/usr/bin/env python3
"""
Elysia Engine 구조 추출 및 평가 스크립트

이 스크립트는 Elysia Engine의 구조를 분석하고,
객관적인 평가 지표와 개선 사항을 보고합니다.

사용법:
    python scripts/extract_structure.py [--format text|mermaid|json]
"""

import argparse
import sys
import os
import json
from datetime import datetime
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from elysia_engine.evaluation import (
    evaluate_structure,
    generate_report,
    StructureVisualizer,
    ModuleCategory,
    QualityLevel
)


def print_header(title: str) -> None:
    """헤더 출력"""
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60 + "\n")


def print_section(title: str) -> None:
    """섹션 제목 출력"""
    print(f"\n{'─' * 40}")
    print(f"📌 {title}")
    print(f"{'─' * 40}\n")


def format_score_bar(score: float, width: int = 30) -> str:
    """점수 막대 생성"""
    filled = int(score * width)
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}] {score:.1%}"


def main():
    parser = argparse.ArgumentParser(
        description="Elysia Engine 구조 추출 및 평가"
    )
    parser.add_argument(
        "--format", "-f",
        choices=["text", "mermaid", "json", "full"],
        default="full",
        help="출력 형식 (기본값: full)"
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        default=None,
        help="출력 파일 경로 (기본값: 표준 출력)"
    )
    
    args = parser.parse_args()
    root_path = str(project_root)
    
    if args.format in ["text", "mermaid", "json"]:
        report = generate_report(root_path, args.format)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(report)
            print(f"보고서가 {args.output}에 저장되었습니다.")
        else:
            print(report)
        return
    
    # Full 보고서
    print_header("🌌 Elysia Engine 구조 평가 보고서")
    print(f"생성 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"저장소 경로: {root_path}")
    
    # 평가 실행
    result = evaluate_structure(root_path)
    
    # 1. 전체 점수
    print_section("📊 전체 평가")
    print(f"품질 등급: {result.quality_level.value}")
    print(f"전체 점수: {format_score_bar(result.overall_score)}")
    
    # 2. 세부 점수
    print_section("📈 세부 점수")
    scores = [
        ("아키텍처", result.architecture_score),
        ("코드 품질", result.code_quality_score),
        ("문서화", result.documentation_score),
        ("테스트 커버리지", result.test_coverage_score),
        ("모듈 연결성", result.connectivity_score),
    ]
    
    for name, score in scores:
        print(f"  {name:15s}: {format_score_bar(score)}")
    
    # 3. 모듈 현황
    print_section("📦 모듈 현황")
    
    # 카테고리별 집계
    category_counts = {}
    for module in result.modules:
        cat = module.category
        if cat not in category_counts:
            category_counts[cat] = {"count": 0, "loc": 0, "classes": 0, "functions": 0}
        category_counts[cat]["count"] += 1
        category_counts[cat]["loc"] += module.lines_of_code
        category_counts[cat]["classes"] += module.class_count
        category_counts[cat]["functions"] += module.function_count
    
    category_icons = {
        ModuleCategory.CORE: "⚙️",
        ModuleCategory.PHYSICS: "🌀",
        ModuleCategory.CONSCIOUSNESS: "🧠",
        ModuleCategory.SYSTEM: "🔧",
        ModuleCategory.INTEGRATION: "🔗",
        ModuleCategory.UTILITY: "🛠️"
    }
    
    print(f"{'카테고리':20s} {'모듈':6s} {'LOC':8s} {'클래스':8s} {'함수':8s}")
    print("-" * 50)
    for cat, stats in sorted(category_counts.items(), key=lambda x: -x[1]["count"]):
        icon = category_icons.get(cat, "📄")
        print(f"{icon} {cat.value:17s} {stats['count']:6d} {stats['loc']:8d} {stats['classes']:8d} {stats['functions']:8d}")
    
    total_modules = len(result.modules)
    total_loc = sum(m.lines_of_code for m in result.modules)
    total_classes = sum(m.class_count for m in result.modules)
    total_functions = sum(m.function_count for m in result.modules)
    print("-" * 50)
    print(f"{'합계':20s} {total_modules:6d} {total_loc:8d} {total_classes:8d} {total_functions:8d}")
    
    # 4. 모듈 구조 트리
    print_section("🌳 모듈 구조")
    visualizer = StructureVisualizer()
    tree = visualizer.generate_ascii_tree({m.name: m for m in result.modules})
    print(tree)
    
    # 5. 관계성 그래프
    print_section("🔗 모듈 관계 (상위 20개)")
    
    # 가장 많은 의존성을 가진 모듈들
    dep_counts = {}
    for module in result.modules:
        dep_counts[module.name] = {
            "deps": len(module.dependencies),
            "dependents": len(module.dependents),
            "total": len(module.dependencies) + len(module.dependents)
        }
    
    sorted_by_connections = sorted(dep_counts.items(), key=lambda x: -x[1]["total"])[:20]
    
    print(f"{'모듈':40s} {'의존':6s} {'피의존':6s} {'총합':6s}")
    print("-" * 60)
    for name, counts in sorted_by_connections:
        short_name = name.split(".")[-1]
        print(f"{short_name:40s} {counts['deps']:6d} {counts['dependents']:6d} {counts['total']:6d}")
    
    # 6. 강점
    print_section("✅ 강점")
    for i, strength in enumerate(result.strengths, 1):
        print(f"  {i}. {strength}")
    
    # 7. 개선 사항
    print_section("🔧 개선 사항")
    
    priority_icons = {"높음": "🔴", "중간": "🟡", "낮음": "🟢"}
    
    for i, imp in enumerate(result.improvements, 1):
        icon = priority_icons.get(imp["priority"], "⚪")
        print(f"\n  {i}. [{icon} {imp['priority']}] {imp['title']}")
        print(f"     카테고리: {imp['category']}")
        print(f"     설명: {imp['description']}")
        print(f"     현재 상태: {imp['status']}")
        print(f"     예상 노력: {imp['estimated_effort']}")
    
    # 8. Mermaid 다이어그램
    print_section("📊 의존성 다이어그램 (Mermaid)")
    mermaid = visualizer.generate_mermaid_diagram(
        {m.name: m for m in result.modules},
        result.relationships
    )
    print(mermaid)
    
    # 9. 요약
    print_section("📝 결론")
    print(result.summary)
    
    # JSON 파일로도 저장
    if args.output:
        json_data = visualizer.generate_json_export(result)
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        print(f"\nJSON 보고서가 {args.output}에 저장되었습니다.")


if __name__ == "__main__":
    main()
