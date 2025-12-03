#!/usr/bin/env python3
"""
Elysia Engine 구조 평가 데모
============================

이 예제는 Elysia Engine의 구조를 분석하고,
객관적인 평가 지표와 개선 사항을 시연합니다.

다른 개발자들과 공유할 때, 이 스크립트를 실행하면
엔진의 현재 상태와 품질을 객관적으로 파악할 수 있습니다.
"""

from pathlib import Path
from elysia_engine import (
    evaluate_structure,
    generate_report,
    StructureVisualizer,
)


def demo_structure_evaluation():
    """구조 평가 데모"""
    
    print("=" * 60)
    print(" 🌌 Elysia Engine 구조 평가 데모")
    print("=" * 60)
    
    # 프로젝트 루트 경로
    root_path = Path(__file__).parent.parent
    
    # 1. 구조 평가 실행
    print("\n📊 구조 분석 중...")
    result = evaluate_structure(str(root_path))
    
    # 2. 결과 요약
    print(f"\n✅ 분석 완료!")
    print(f"   - 분석된 모듈: {len(result.modules)}개")
    print(f"   - 발견된 관계: {len(result.relationships)}개")
    print(f"   - 전체 품질: {result.quality_level.value}")
    print(f"   - 점수: {result.overall_score:.2f}")
    
    # 3. 세부 점수
    print("\n📈 세부 점수:")
    print(f"   아키텍처:      {result.architecture_score:.1%}")
    print(f"   코드 품질:     {result.code_quality_score:.1%}")
    print(f"   문서화:        {result.documentation_score:.1%}")
    print(f"   테스트 커버리지: {result.test_coverage_score:.1%}")
    print(f"   모듈 연결성:   {result.connectivity_score:.1%}")
    
    # 4. 강점
    print("\n✨ 강점 (상위 5개):")
    for i, strength in enumerate(result.strengths[:5], 1):
        print(f"   {i}. {strength}")
    
    # 5. 개선 사항
    print("\n🔧 개선 사항 (상위 3개):")
    for i, imp in enumerate(result.improvements[:3], 1):
        print(f"   {i}. [{imp['priority']}] {imp['title']}")
        print(f"      → {imp['description']}")
    
    # 6. 카테고리별 모듈 수
    from collections import Counter
    categories = Counter(m.category.value for m in result.modules)
    print("\n📦 카테고리별 모듈 수:")
    for cat, count in categories.most_common():
        print(f"   {cat}: {count}개")
    
    # 7. Mermaid 다이어그램 샘플
    print("\n📊 의존성 다이어그램 (Mermaid 형식):")
    mermaid = StructureVisualizer.generate_mermaid_diagram(
        {m.name: m for m in result.modules[:10]},  # 상위 10개만
        result.relationships[:20]  # 상위 20개 관계만
    )
    print(mermaid)
    
    print("\n" + "=" * 60)
    print(" 자세한 보고서: python scripts/extract_structure.py --format full")
    print("=" * 60)


def demo_json_export():
    """JSON 내보내기 데모"""
    
    print("\n📄 JSON 보고서 생성...")
    
    root_path = Path(__file__).parent.parent
    json_report = generate_report(str(root_path), "json")
    
    # 보고서 크기
    size_kb = len(json_report) / 1024
    print(f"   생성된 JSON 크기: {size_kb:.1f} KB")
    
    # 샘플 출력 (처음 500자)
    print("\n   샘플 (처음 500자):")
    print("   " + json_report[:500].replace("\n", "\n   ") + "...")


def demo_use_in_code():
    """코드에서 사용하는 예제"""
    
    print("\n💻 코드에서 사용하기:")
    print("""
    from elysia_engine import evaluate_structure, ModuleCategory
    
    # 1. 구조 평가
    result = evaluate_structure("/path/to/project")
    
    # 2. 점수 확인
    print(f"전체 점수: {result.overall_score:.1%}")
    
    # 3. 핵심 모듈 필터링
    core_modules = [
        m for m in result.modules 
        if m.category == ModuleCategory.CORE
    ]
    
    # 4. 개선 사항 확인
    for imp in result.improvements:
        if imp["priority"] == "높음":
            print(f"우선 개선: {imp['title']}")
    """)


if __name__ == "__main__":
    demo_structure_evaluation()
    demo_json_export()
    demo_use_in_code()
