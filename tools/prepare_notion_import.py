from __future__ import annotations

import json
import os
import re
import shutil
from pathlib import Path


ROOT = Path(r"C:\obsidian-vault")
SOURCE_ROOT = ROOT / "에이전트"
IMAGE_ROOT = ROOT / "image"
OUTPUT_ROOT = ROOT / "notion_import" / "Heat Grid Agent"


DOC_SUMMARIES = {
    "Heat_Grid_Agent": [
        "Heat Grid Agent 전체 설계와 문서 연결 구조를 빠르게 파악하기 위한 시작 페이지입니다.",
        "자동감지 에이전트와 운영보조 에이전트, 시뮬레이션 결과 문서를 한 흐름으로 묶습니다.",
    ],
    "heat_grid_agent_auto": [
        "자동감지 에이전트의 입력-모델-출력 구조를 요약한 개요 문서입니다.",
        "1번~4번 흐름과 보충 설명 문서를 따라 우선순위 산정 로직을 읽을 수 있습니다.",
    ],
    "heat_grid_agent_ops": [
        "운영보조 에이전트가 참조하는 DB 구조와 JSON 설계를 정리한 개요 문서입니다.",
        "Raw, model, Priority, OPS 데이터가 어떤 순서로 연결되는지 보여줍니다.",
    ],
    "v1_minimal_ops 결과 보고서": [
        "최소 운영 시나리오 기준으로 시뮬레이션 결과를 정리한 보고서입니다.",
        "실행 결과와 해석 포인트를 팀이 빠르게 확인할 수 있도록 보존합니다.",
    ],
}


FOLDER_SUMMARIES = {
    "01_자동감지 에이전트": [
        "자동감지 에이전트 관련 문서를 모아둔 상위 페이지입니다.",
        "개요, 흐름 문서, 보충 설명을 순서대로 따라가며 우선순위 로직을 이해할 수 있습니다.",
    ],
    "02_운영보조 에이전트": [
        "운영보조 에이전트 관련 문서를 모아둔 상위 페이지입니다.",
        "DB 구조, 입력/출력 스키마, 예시 JSON을 중심으로 운영 흐름을 파악할 수 있습니다.",
    ],
    "시뮬레이션": [
        "실험 및 운영 시뮬레이션 결과 문서를 모아둔 상위 페이지입니다.",
        "현재는 `v1_minimal_ops 결과 보고서`를 대표 문서로 사용합니다.",
    ],
    "흐름": [
        "자동감지 에이전트의 단계별 우선순위 계산 흐름을 모아둔 페이지입니다.",
        "1번 흐름부터 4번 흐름까지 순서대로 읽는 것을 권장합니다.",
    ],
    "보충 설명": [
        "핵심 흐름에서 참조하는 세부 개념과 파라미터 설명을 모아둔 페이지입니다.",
        "가중치, 게이트, 윈도우, 레벨 기준 같은 보조 개념을 확인할 수 있습니다.",
    ],
    "순서": [
        "운영보조 에이전트 데이터 문서를 순서별로 모아둔 페이지입니다.",
        "Raw → model → Priority → OPS 흐름과 스키마 문서를 함께 읽을 수 있습니다.",
    ],
    "예시": [
        "운영보조 에이전트 입출력 예시 JSON을 모아둔 페이지입니다.",
        "스키마 문서와 함께 실제 값 예시를 빠르게 확인할 수 있습니다.",
    ],
}


def slug_name(name: str) -> str:
    return name


def first_nonempty_line(text: str) -> str:
    for line in text.splitlines():
        if line.strip():
            return line.strip()
    return ""


def summarize_doc(name: str, text: str, links: list[str]) -> list[str]:
    if name in DOC_SUMMARIES:
        return DOC_SUMMARIES[name]

    first = first_nonempty_line(text)
    first = re.sub(r"^#+\s*", "", first).strip()
    summary = []
    if first:
        summary.append(f"이 문서는 `{first}`를 중심으로 정리된 세부 설명입니다.")
    if links:
        joined = ", ".join(f"`{link}`" for link in links[:4])
        summary.append(f"관련 문서: {joined}")
    else:
        summary.append("관련 하위 링크 없이 단일 설명 또는 예시를 보존하는 문서입니다.")
    return summary[:2]


def convert_wikilinks(
    text: str,
    current_output_file: Path,
    page_targets: dict[str, Path],
    image_targets: dict[str, Path],
    unresolved: list[str],
) -> str:
    def replace_embed(match: re.Match[str]) -> str:
        raw = match.group(1).strip()
        name = raw.split("|", 1)[0].strip()
        if name in image_targets:
            rel = os.path.relpath(image_targets[name], start=current_output_file.parent).replace("\\", "/")
            return f"![]({rel})"
        unresolved.append(f"missing-image:{name}")
        return f"`[원문 이미지 확인 필요: {name}]`"

    def replace_link(match: re.Match[str]) -> str:
        raw = match.group(1).strip()
        target = raw.split("|", 1)[0].strip()
        anchor = ""
        if "#" in target:
            target, anchor = target.split("#", 1)
        target = target.strip()
        label = target.split("/")[-1].strip() or target

        if target in page_targets:
            rel = os.path.relpath(page_targets[target], start=current_output_file.parent).replace("\\", "/")
            if anchor:
                return f"[{label}]({rel}#{anchor})"
            return f"[{label}]({rel})"

        if label in page_targets:
            rel = os.path.relpath(page_targets[label], start=current_output_file.parent).replace("\\", "/")
            if anchor:
                return f"[{label}]({rel}#{anchor})"
            return f"[{label}]({rel})"

        unresolved.append(f"missing-link:{target}")
        return f"`[원문 링크 확인 필요: {target}]`"

    text = re.sub(r"!\[\[([^\]]+)\]\]", replace_embed, text)
    text = re.sub(r"\[\[([^\]]+)\]\]", replace_link, text)
    return text


def build_folder_page(folder: Path, children: list[Path]) -> str:
    summary_lines = FOLDER_SUMMARIES.get(folder.name, [f"`{folder.name}` 관련 문서를 모아둔 상위 페이지입니다."])
    child_lines = [f"- [{child.stem}]({child.name})" for child in sorted(children, key=lambda p: p.name)]
    lines = [
        f"# {folder.name}",
        "",
        "## 요약",
        *[f"- {line}" for line in summary_lines],
        "",
        "## 하위 문서",
    ]
    lines.extend(child_lines if child_lines else ["- 하위 문서 없음"])
    lines.append("")
    return "\n".join(lines)


def folder_page_filename(folder: Path, existing_docs: list[Path]) -> str:
    base = f"{folder.name}.md"
    if any(doc.name == base for doc in existing_docs):
        return f"{folder.name} 허브.md"
    return base


def main() -> None:
    if OUTPUT_ROOT.exists():
        shutil.rmtree(OUTPUT_ROOT)
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)

    image_output_root = OUTPUT_ROOT / "image"
    shutil.copytree(IMAGE_ROOT, image_output_root)

    source_docs = sorted(SOURCE_ROOT.rglob("*.md"))
    page_targets: dict[str, Path] = {}
    by_folder: dict[Path, list[Path]] = {}

    for src in source_docs:
        rel = src.relative_to(SOURCE_ROOT)
        out = OUTPUT_ROOT / rel
        page_targets[src.stem] = out
        page_targets[rel.with_suffix("").as_posix()] = out
        by_folder.setdefault(out.parent, []).append(out)

    image_targets = {p.name: p for p in image_output_root.rglob("*") if p.is_file()}
    unresolved: dict[str, list[str]] = {}

    for src in source_docs:
        rel = src.relative_to(SOURCE_ROOT)
        out = OUTPUT_ROOT / rel
        out.parent.mkdir(parents=True, exist_ok=True)

        text = src.read_text(encoding="utf-8")
        links = re.findall(r"\[\[([^\]|#]+)", text)
        summary = summarize_doc(src.stem, text, links)
        current_unresolved: list[str] = []
        converted = convert_wikilinks(text, out, page_targets, image_targets, current_unresolved)

        doc = [
            f"# {src.stem}",
            "",
            "## 요약",
            *[f"- {line}" for line in summary],
            "",
            "## 원문",
            "",
            converted.strip(),
            "",
        ]
        out.write_text("\n".join(doc), encoding="utf-8")
        if current_unresolved:
            unresolved[str(rel)] = current_unresolved

    folders = sorted({path.parent for path in page_targets.values()}, key=lambda p: len(p.parts), reverse=True)
    for folder in folders:
        if folder == OUTPUT_ROOT:
            continue
        child_docs = [p for p in folder.iterdir() if p.is_file() and p.suffix == ".md"]
        folder_page = folder / folder_page_filename(folder, child_docs)
        child_targets = [p for p in child_docs if p.name != folder_page.name]
        folder_page.write_text(build_folder_page(folder, child_targets), encoding="utf-8")

    hub = OUTPUT_ROOT / "Heat Grid Agent Hub.md"
    hub.write_text(
        "\n".join(
            [
                "# Heat Grid Agent",
                "",
                "## 개요",
                "- Heat Grid Agent 관련 옵시디언 문서를 팀이 읽기 쉬운 노션용 구조로 정리한 허브입니다.",
                "- 자동감지 에이전트, 운영보조 에이전트, 시뮬레이션 결과를 한 페이지 맵에서 연결합니다.",
                "",
                "## 문서 지도",
                "- [01_자동감지 에이전트](01_자동감지 에이전트/01_자동감지 에이전트.md)",
                "- [02_운영보조 에이전트](02_운영보조 에이전트/02_운영보조 에이전트.md)",
                "- [시뮬레이션](시뮬레이션/시뮬레이션.md)",
                "",
                "## 추천 읽기 순서",
                "1. `01_자동감지 에이전트/heat_grid_agent_auto`",
                "2. `01_자동감지 에이전트/흐름` 문서들",
                "3. `02_운영보조 에이전트/heat_grid_agent_ops`",
                "4. `02_운영보조 에이전트/순서` 및 예시 JSON",
                "5. `시뮬레이션/v1_minimal_ops 결과 보고서`",
                "",
            ]
        ),
        encoding="utf-8",
    )

    report = {
        "output_root": str(OUTPUT_ROOT),
        "source_docs": len(source_docs),
        "unresolved": unresolved,
    }
    (OUTPUT_ROOT / "_migration_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
