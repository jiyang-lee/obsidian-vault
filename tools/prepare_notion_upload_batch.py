from __future__ import annotations

import os
import re
import shutil
from pathlib import Path


ROOT = Path(r"C:\obsidian-vault")
SOURCE_ROOT = ROOT / "에이전트"
IMAGE_ROOT = ROOT / "image"
OUT_ROOT = ROOT / "notion_upload_batch"


FILES = {
    "01_허브_Heat_Grid_Agent.md": [
        SOURCE_ROOT / "Heat_Grid_Agent.md",
        SOURCE_ROOT / "에이전트 목록.md",
    ],
    "02_자동감지_개요.md": [
        SOURCE_ROOT / "01_자동감지 에이전트" / "heat_grid_agent_auto" / "heat_grid_agent_auto.md",
        SOURCE_ROOT / "01_자동감지 에이전트" / "heat_grid_agent_auto" / "부족.md",
    ],
    "03_자동감지_흐름.md": [
        SOURCE_ROOT / "01_자동감지 에이전트" / "heat_grid_agent_auto" / "흐름" / "1번 흐름.md",
        SOURCE_ROOT / "01_자동감지 에이전트" / "heat_grid_agent_auto" / "흐름" / "2번 흐름.md",
        SOURCE_ROOT / "01_자동감지 에이전트" / "heat_grid_agent_auto" / "흐름" / "3번 흐름.md",
        SOURCE_ROOT / "01_자동감지 에이전트" / "heat_grid_agent_auto" / "흐름" / "4번 흐름.md",
    ],
    "04_자동감지_보충설명.md": sorted((SOURCE_ROOT / "01_자동감지 에이전트" / "heat_grid_agent_auto" / "흐름" / "보충 설명").glob("*.md")),
    "05_운영보조_개요.md": [
        SOURCE_ROOT / "02_운영보조 에이전트" / "heat_grid_agent_ops" / "heat_grid_agent_ops.md",
    ],
    "06_운영보조_데이터구조.md": [
        SOURCE_ROOT / "02_운영보조 에이전트" / "heat_grid_agent_ops" / "순서" / "Raw Data.md",
        SOURCE_ROOT / "02_운영보조 에이전트" / "heat_grid_agent_ops" / "순서" / "model Data.md",
        SOURCE_ROOT / "02_운영보조 에이전트" / "heat_grid_agent_ops" / "순서" / "Priority Data.md",
        SOURCE_ROOT / "02_운영보조 에이전트" / "heat_grid_agent_ops" / "순서" / "OPS Data.md",
        SOURCE_ROOT / "02_운영보조 에이전트" / "heat_grid_agent_ops" / "순서" / "보충 설명" / "feature_meta_map.md",
    ],
    "07_운영보조_스키마와예시.md": [
        SOURCE_ROOT / "02_운영보조 에이전트" / "heat_grid_agent_ops" / "순서" / "ops_agent_input.schema.json.md",
        SOURCE_ROOT / "02_운영보조 에이전트" / "heat_grid_agent_ops" / "순서" / "ops_agent_output.schema.json.md",
        SOURCE_ROOT / "02_운영보조 에이전트" / "heat_grid_agent_ops" / "순서" / "예시" / "ops_agent_input.json.md",
        SOURCE_ROOT / "02_운영보조 에이전트" / "heat_grid_agent_ops" / "순서" / "예시" / "ops_agent_output.json.md",
        SOURCE_ROOT / "02_운영보조 에이전트" / "heat_grid_agent_ops" / "순서" / "예시" / "priority_context.json.md",
        SOURCE_ROOT / "02_운영보조 에이전트" / "heat_grid_agent_ops" / "순서" / "예시" / "raw_context.json.md",
    ],
    "08_시뮬레이션.md": [
        SOURCE_ROOT / "시뮬레이션" / "v0_minimal_ops" / "v0 결과 보고서.md",
    ],
}


INTRO = {
    "01_허브_Heat_Grid_Agent.md": [
        "Heat Grid Agent 전체 문서 맵입니다.",
        "자동감지 에이전트, 운영보조 에이전트, 시뮬레이션 결과를 팀이 바로 읽을 수 있게 묶었습니다.",
    ],
    "02_자동감지_개요.md": [
        "자동감지 에이전트의 전체 개요와 부족한 점 메모를 함께 정리한 문서입니다.",
        "입력-모델-출력 구조와 흐름 문서의 진입점을 제공합니다.",
    ],
    "03_자동감지_흐름.md": [
        "자동감지 에이전트의 1번~4번 흐름을 한 문서에 모았습니다.",
        "우선순위 산정 로직을 순서대로 검토할 때 사용하는 묶음입니다.",
    ],
    "04_자동감지_보충설명.md": [
        "자동감지 흐름에서 참조하는 세부 개념 문서를 모았습니다.",
        "가중치, 게이트, 윈도우, 레벨 기준 같은 설명을 보존합니다.",
    ],
    "05_운영보조_개요.md": [
        "운영보조 에이전트의 DB 구조와 JSON 설계 개요입니다.",
        "관련 데이터 문서와 스키마 문서의 진입점 역할을 합니다.",
    ],
    "06_운영보조_데이터구조.md": [
        "운영보조 에이전트의 데이터 흐름 문서를 한 묶음으로 정리했습니다.",
        "Raw, model, Priority, OPS 데이터와 보충 설명을 포함합니다.",
    ],
    "07_운영보조_스키마와예시.md": [
        "운영보조 에이전트의 입력/출력 스키마와 예시 JSON을 함께 정리했습니다.",
        "팀이 실제 입출력 형태를 빠르게 확인할 수 있습니다.",
    ],
    "08_시뮬레이션.md": [
        "시뮬레이션 결과 보고서를 보존한 문서입니다.",
        "운영 시나리오 결과와 해석 메모를 함께 확인합니다.",
    ],
}


def rel_image_path(output_file: Path, image_name: str) -> str:
    src = OUT_ROOT / "image" / image_name
    return os.path.relpath(src, start=output_file.parent).replace("\\", "/")


def convert_content(text: str, output_file: Path) -> str:
    def repl_embed(match: re.Match[str]) -> str:
        name = match.group(1).split("|", 1)[0].strip()
        candidate = OUT_ROOT / "image" / name
        if candidate.exists():
            return f"![]({rel_image_path(output_file, name)})"
        return f"`[원문 이미지 확인 필요: {name}]`"

    def repl_link(match: re.Match[str]) -> str:
        raw = match.group(1).split("|", 1)[0].strip()
        label = raw.split("/")[-1]
        return f"`{label}`"

    text = re.sub(r"!\[\[([^\]]+)\]\]", repl_embed, text)
    text = re.sub(r"\[\[([^\]]+)\]\]", repl_link, text)
    return text


def main() -> None:
    if OUT_ROOT.exists():
        shutil.rmtree(OUT_ROOT)
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    shutil.copytree(IMAGE_ROOT, OUT_ROOT / "image")

    for filename, source_files in FILES.items():
        out = OUT_ROOT / filename
        parts: list[str] = [f"# {Path(filename).stem}", "", "## 요약"]
        parts.extend(f"- {line}" for line in INTRO[filename])
        parts.append("")

        for source in source_files:
            text = source.read_text(encoding="utf-8")
            title = source.stem
            parts.append(f"---\n\n## {title}\n")
            parts.append(convert_content(text.strip(), out))
            parts.append("")

        out.write_text("\n".join(parts), encoding="utf-8")


if __name__ == "__main__":
    main()
