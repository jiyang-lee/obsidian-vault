from __future__ import annotations

import base64
import html
import re
import shutil
from pathlib import Path


ROOT = Path(r"C:\obsidian-vault")
SOURCE_ROOT = ROOT / "에이전트"
IMAGE_ROOT = ROOT / "image"
OUT_ROOT = ROOT / "notion_html_import"


PAGES = {
    "02_자동감지_개요.html": {
        "sources": [
            SOURCE_ROOT / "01_자동감지 에이전트" / "heat_grid_agent_auto" / "heat_grid_agent_auto.md",
            SOURCE_ROOT / "01_자동감지 에이전트" / "heat_grid_agent_auto" / "부족.md",
        ],
        "images": ["image.png", "Pasted image 20260706171434.png"],
        "summary": [
            "자동감지 에이전트의 전체 개요와 부족한 점 메모를 함께 정리한 문서입니다.",
            "입력-모델-출력 구조와 흐름 문서의 진입점을 제공합니다.",
        ],
    },
    "03_자동감지_흐름.html": {
        "sources": [
            SOURCE_ROOT / "01_자동감지 에이전트" / "heat_grid_agent_auto" / "흐름" / "1번 흐름.md",
            SOURCE_ROOT / "01_자동감지 에이전트" / "heat_grid_agent_auto" / "흐름" / "2번 흐름.md",
            SOURCE_ROOT / "01_자동감지 에이전트" / "heat_grid_agent_auto" / "흐름" / "3번 흐름.md",
            SOURCE_ROOT / "01_자동감지 에이전트" / "heat_grid_agent_auto" / "흐름" / "4번 흐름.md",
        ],
        "images": [
            "image (1).png",
            "image (2).png",
            "image (3).png",
            "Pasted image 20260706155612.png",
            "Pasted image 20260706164723.png",
            "Pasted image 20260706165536.png",
            "Pasted image 20260706171824.png",
        ],
        "summary": [
            "자동감지 에이전트의 1번~4번 흐름을 모은 문서입니다.",
            "우선순위 계산 로직을 단계별로 읽을 수 있습니다.",
        ],
    },
    "04_자동감지_보충설명.html": {
        "sources": sorted((SOURCE_ROOT / "01_자동감지 에이전트" / "heat_grid_agent_auto" / "흐름" / "보충 설명").glob("*.md")),
        "images": ["Pasted image 20260706160522.png", "Pasted image 20260706162013.png"],
        "summary": [
            "자동감지 흐름에서 참조하는 보충 설명을 모았습니다.",
            "가중치, 윈도우, 게이트, 레벨 기준 같은 세부 개념을 확인할 수 있습니다.",
        ],
    },
    "05_운영보조_개요.html": {
        "sources": [SOURCE_ROOT / "02_운영보조 에이전트" / "heat_grid_agent_ops" / "heat_grid_agent_ops.md"],
        "images": ["Pasted image 20260706203027.png", "Pasted image 20260706210520.png", "Pasted image 20260706211839.png"],
        "summary": [
            "운영보조 에이전트의 DB 구조와 JSON 설계 개요입니다.",
            "관련 데이터 문서와 스키마 문서의 진입점 역할을 합니다.",
        ],
    },
    "06_운영보조_데이터구조.html": {
        "sources": [
            SOURCE_ROOT / "02_운영보조 에이전트" / "heat_grid_agent_ops" / "순서" / "Raw Data.md",
            SOURCE_ROOT / "02_운영보조 에이전트" / "heat_grid_agent_ops" / "순서" / "model Data.md",
            SOURCE_ROOT / "02_운영보조 에이전트" / "heat_grid_agent_ops" / "순서" / "Priority Data.md",
            SOURCE_ROOT / "02_운영보조 에이전트" / "heat_grid_agent_ops" / "순서" / "OPS Data.md",
            SOURCE_ROOT / "02_운영보조 에이전트" / "heat_grid_agent_ops" / "순서" / "보충 설명" / "feature_meta_map.md",
        ],
        "images": ["Pasted image 20260706200426.png", "Pasted image 20260706202154.png", "Pasted image 20260706202602.png", "Pasted image 20260706210749.png"],
        "summary": [
            "운영보조 에이전트의 데이터 흐름 문서를 정리한 문서입니다.",
            "Raw, model, Priority, OPS 데이터와 보충 설명을 포함합니다.",
        ],
    },
    "07_운영보조_스키마와예시.html": {
        "sources": [
            SOURCE_ROOT / "02_운영보조 에이전트" / "heat_grid_agent_ops" / "순서" / "ops_agent_input.schema.json.md",
            SOURCE_ROOT / "02_운영보조 에이전트" / "heat_grid_agent_ops" / "순서" / "ops_agent_output.schema.json.md",
            SOURCE_ROOT / "02_운영보조 에이전트" / "heat_grid_agent_ops" / "순서" / "예시" / "ops_agent_input.json.md",
            SOURCE_ROOT / "02_운영보조 에이전트" / "heat_grid_agent_ops" / "순서" / "예시" / "ops_agent_output.json.md",
            SOURCE_ROOT / "02_운영보조 에이전트" / "heat_grid_agent_ops" / "순서" / "예시" / "priority_context.json.md",
            SOURCE_ROOT / "02_운영보조 에이전트" / "heat_grid_agent_ops" / "순서" / "예시" / "raw_context.json.md",
        ],
        "images": ["Pasted image 20260706215700.png", "Pasted image 20260706215725.png", "Pasted image 20260706215805.png"],
        "summary": [
            "운영보조 에이전트의 입력/출력 스키마와 예시 JSON을 모았습니다.",
            "실제 입출력 형태를 빠르게 확인할 수 있습니다.",
        ],
    },
}


def sanitize(text: str) -> str:
    text = re.sub(r"!\[\[[^\]]+\]\]", "[이미지 복구본은 아래 이미지 섹션을 확인하세요]", text)
    text = re.sub(r"\[\[([^\]]+)\]\]", r"\1", text)
    return html.escape(text)


def image_html(image_name: str) -> str:
    data = base64.b64encode((IMAGE_ROOT / image_name).read_bytes()).decode("ascii")
    return (
        '<figure style="margin:24px 0;">'
        f'<img alt="{html.escape(image_name)}" src="data:image/png;base64,{data}" '
        'style="max-width:100%; height:auto; border:1px solid #ddd; border-radius:8px;" />'
        f'<figcaption style="font-size:12px; color:#666; margin-top:8px;">{html.escape(image_name)}</figcaption>'
        '</figure>'
    )


def page_html(title: str, summary: list[str], sections: list[tuple[str, str]], images: list[str]) -> str:
    summary_html = "".join(f"<li>{html.escape(line)}</li>" for line in summary)
    section_html = ""
    for name, text in sections:
        section_html += f"<h2>{html.escape(name)}</h2><pre>{sanitize(text)}</pre>"
    images_html = "".join(image_html(name) for name in images)
    return f"""<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8" />
  <title>{html.escape(title)}</title>
  <style>
    body {{ font-family: Arial, sans-serif; line-height: 1.6; max-width: 960px; margin: 40px auto; padding: 0 24px; }}
    h1, h2 {{ color: #1f2937; }}
    pre {{ white-space: pre-wrap; word-break: break-word; background: #f8fafc; border: 1px solid #e5e7eb; border-radius: 8px; padding: 16px; }}
    ul {{ margin-top: 0; }}
  </style>
</head>
<body>
  <h1>{html.escape(title)}</h1>
  <h2>요약</h2>
  <ul>{summary_html}</ul>
  {section_html}
  <h2>이미지</h2>
  {images_html}
</body>
</html>
"""


def main() -> None:
    if OUT_ROOT.exists():
        shutil.rmtree(OUT_ROOT)
    OUT_ROOT.mkdir(parents=True, exist_ok=True)

    for filename, config in PAGES.items():
        sections = []
        for source in config["sources"]:
            sections.append((source.stem, source.read_text(encoding="utf-8")))
        title = Path(filename).stem
        html_doc = page_html(title, config["summary"], sections, config["images"])
        (OUT_ROOT / filename).write_text(html_doc, encoding="utf-8")


if __name__ == "__main__":
    main()
