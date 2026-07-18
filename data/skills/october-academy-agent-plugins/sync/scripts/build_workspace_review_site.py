#!/usr/bin/env python3
"""Build an HTTP-friendly review site for the blog-figure workspace outputs."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path


REVIEW_CARD_CSS = """
:root {
  color-scheme: dark;
}
* {
  box-sizing: border-box;
}
body {
  margin: 0;
  padding: 32px;
  font-family: "Noto Sans KR", system-ui, sans-serif;
  background:
    radial-gradient(circle at top, rgba(255, 107, 53, 0.12), transparent 24rem),
    linear-gradient(180deg, #121212 0%, #0b0b0b 100%);
  color: #f5f5f5;
}
h1 {
  margin: 0 0 8px;
  font-size: 2rem;
}
p.lede {
  margin: 0 0 24px;
  max-width: 72rem;
  color: #b5b5b5;
}
.summary {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 28px;
}
.chip {
  border: 1px solid #333;
  border-radius: 999px;
  padding: 8px 12px;
  background: rgba(255, 255, 255, 0.04);
  color: #d8d8d8;
  font-size: 0.95rem;
}
.grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 20px;
}
.card {
  border: 1px solid #303030;
  border-radius: 18px;
  padding: 16px;
  background: rgba(17, 17, 17, 0.86);
  backdrop-filter: blur(6px);
  box-shadow: 0 16px 48px rgba(0, 0, 0, 0.28);
}
.meta {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 12px;
  align-items: baseline;
}
.title-wrap {
  min-width: 0;
}
.pattern-id {
  display: inline-block;
  margin-bottom: 6px;
  border-radius: 999px;
  padding: 4px 8px;
  background: #1f1f1f;
  color: #ffcf8c;
  font-size: 0.82rem;
  font-family: "JetBrains Mono", ui-monospace, monospace;
}
.pattern-name {
  display: block;
  font-weight: 800;
  font-size: 1rem;
  word-break: break-word;
}
.src {
  color: #8b8b8b;
  font-size: 0.75rem;
  font-family: "JetBrains Mono", ui-monospace, monospace;
  text-align: right;
}
.frame-shell {
  width: min(100%, 360px);
  aspect-ratio: 16 / 9;
  overflow: hidden;
  border: 1px solid #3c3c3c;
  border-radius: 12px;
  background: #f5f5f5;
  margin: 0 auto;
}
.frame-shell iframe {
  width: 1440px;
  height: 810px;
  border: 0;
  transform: scale(0.25);
  transform-origin: top left;
  display: block;
}
.links {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  margin-top: 10px;
  font-size: 0.82rem;
}
.links a {
  color: #b3e16b;
  text-decoration: none;
}
.links a:hover {
  text-decoration: underline;
}
@media (max-width: 1180px) {
  body {
    padding: 20px;
  }
  .grid {
    grid-template-columns: 1fr;
  }
}
"""


def parse_args() -> argparse.Namespace:
    skill_dir = Path(__file__).resolve().parent.parent
    default_workspace = skill_dir.parent / "blog-figure-workspace"
    parser = argparse.ArgumentParser(
        description="Build a review site for the 30 blog-figure workspace outputs."
    )
    parser.add_argument(
        "--workspace",
        type=Path,
        default=default_workspace,
        help="Path to blog-figure-workspace",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=default_workspace / "review",
        help="Output directory for the generated review site",
    )
    return parser.parse_args()


def load_evals(workspace: Path) -> list[dict]:
    evals_path = workspace / "evals" / "evals.json"
    data = json.loads(evals_path.read_text())
    return data["evals"]


def resolve_source_html(workspace: Path, eval_name: str) -> Path:
    candidates = [
        workspace / "final-test" / eval_name / "figure.html",
        workspace / "iteration-3" / eval_name / "with_skill" / "outputs" / "figure.html",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError(f"Missing HTML output for {eval_name}")


def inline_css(html: str, css_text: str) -> str:
    link_pattern = re.compile(
        r"\s*<link[^>]+href=[\"'][^\"']*figure\.css[^\"']*[\"'][^>]*>\s*",
        flags=re.IGNORECASE,
    )
    html = re.sub(link_pattern, "\n", html)
    style_tag = f"<style>\n{css_text}\n</style>\n"
    if "</head>" in html:
        return html.replace("</head>", f"{style_tag}</head>", 1)
    return f"{style_tag}{html}"


def build_index(entries: list[dict]) -> str:
    cards = []
    for entry in entries:
        cards.append(
            f"""
            <section class="card">
              <div class="meta">
                <div class="title-wrap">
                  <span class="pattern-id">#{entry["id"]:02d}</span>
                  <span class="pattern-name">{entry["name"]}</span>
                </div>
                <div class="src">{entry["source"]}</div>
              </div>
              <div class="frame-shell">
                <iframe src="figures/{entry["slug"]}.html" loading="eager"></iframe>
              </div>
              <div class="links">
                <a href="figures/{entry["slug"]}.html" target="_blank" rel="noreferrer">Open Review Copy</a>
                <a href="{entry["original_href"]}" target="_blank" rel="noreferrer">Open Original</a>
              </div>
            </section>
            """.strip()
        )

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Blog Figure Review</title>
  <style>
  {REVIEW_CARD_CSS}
  </style>
</head>
<body>
  <h1>Blog Figure Review</h1>
  <p class="lede">
    final-test 10개와 iteration-3 20개를 모아 총 30개 Figure를 한 번에 검수한다.
    각 카드는 MCP/브라우저 친화적으로 CSS를 인라인한 review copy를 iframe으로 보여준다.
  </p>
  <div class="summary">
    <div class="chip">30 patterns</div>
    <div class="chip">HTTP-friendly inline CSS</div>
    <div class="chip">Source links preserved</div>
  </div>
  <div class="grid">
    {"".join(cards)}
  </div>
</body>
</html>
"""


def main() -> None:
    args = parse_args()
    workspace = args.workspace.resolve()
    output = args.output.resolve()

    # dev 전용 도구: blog-figure-workspace(30개 eval 산출물)는 배포 플러그인에 포함되지
    # 않는다. workspace가 없으면 FileNotFoundError로 죽지 말고 무엇이 없는지 안내하고 종료.
    if not workspace.exists() or not (workspace / "evals" / "evals.json").exists():
        print(
            "이 스크립트는 dev 전용 도구입니다 — 30개 eval 산출물이 담긴\n"
            "blog-figure-workspace가 있을 때만 review 사이트를 만들 수 있습니다.\n"
            "설치된 플러그인에는 workspace가 포함되지 않으므로 일반 사용에는 필요 없습니다.\n"
            f"  찾은 경로: {workspace}\n"
            "  (필요한 파일: evals/evals.json 와 final-test/… 또는 iteration-3/… 산출물)\n"
            "workspace 위치가 다르면 --workspace 로 직접 지정하세요.",
            file=sys.stderr,
        )
        raise SystemExit(1)

    skill_dir = Path(__file__).resolve().parent.parent
    css_text = (skill_dir / "assets" / "figure.css").read_text()
    evals = load_evals(workspace)

    if output.exists():
        shutil.rmtree(output)
    figures_dir = output / "figures"
    figures_dir.mkdir(parents=True)

    entries: list[dict] = []
    for item in evals:
        src = resolve_source_html(workspace, item["name"])
        slug = f"{item['id']:02d}-{item['name']}"
        html = src.read_text()
        review_html = inline_css(html, css_text)
        (figures_dir / f"{slug}.html").write_text(review_html)
        entries.append(
            {
                "id": item["id"],
                "name": item["name"],
                "slug": slug,
                "source": src.relative_to(workspace).as_posix(),
                "original_href": "../" + src.relative_to(workspace).as_posix(),
            }
        )

    index_html = build_index(entries)
    (output / "index.html").write_text(index_html)
    manifest = [{"id": e["id"], "name": e["name"], "review": f"figures/{e['slug']}.html"} for e in entries]
    (output / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2))

    print(f"Review site written to {output}")
    print(f"Open: {output / 'index.html'}")


if __name__ == "__main__":
    main()
