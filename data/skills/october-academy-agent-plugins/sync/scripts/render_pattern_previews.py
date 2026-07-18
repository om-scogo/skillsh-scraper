#!/usr/bin/env python3
"""Render all blog-figure reference patterns into local preview HTML files."""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
from dataclasses import dataclass, asdict
from pathlib import Path


PATTERN_FILES = (
    ("Layout", "patterns-layout.md"),
    ("Data Viz", "patterns-dataviz-static.md"),
    ("Data Viz", "patterns-dataviz-dynamic.md"),
    ("Visual", "patterns-visual.md"),
)

HEADING_RE = re.compile(r"^##\s+(\d+)\.\s+(.+?)(?:\s+\(|$)", re.MULTILINE)
HTML_BLOCK_RE = re.compile(r"```html\n(.*?)```", re.DOTALL)
PREVIEW_CSS_PATH = "./_assets/figure.css"


@dataclass(frozen=True)
class Pattern:
    number: int
    name: str
    slug: str
    category: str
    source_file: str
    html: str


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def parse_patterns(skill_dir: Path) -> list[Pattern]:
    patterns: list[Pattern] = []
    references_dir = skill_dir / "references"

    for category, filename in PATTERN_FILES:
        text = (references_dir / filename).read_text(encoding="utf-8")
        matches = list(HEADING_RE.finditer(text))
        for index, match in enumerate(matches):
            section_start = match.end()
            section_end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
            section = text[section_start:section_end]
            html_match = HTML_BLOCK_RE.search(section)
            if not html_match:
                raise ValueError(f"Missing HTML example for {filename}::{match.group(2)}")

            number = int(match.group(1))
            name = match.group(2).strip()
            patterns.append(
                Pattern(
                    number=number,
                    name=name,
                    slug=slugify(name),
                    category=category,
                    source_file=filename,
                    html=html_match.group(1).strip(),
                )
            )

    patterns.sort(key=lambda item: item.number)
    return patterns


def extract_body(html_source: str) -> str:
    body_match = re.search(r"<body[^>]*>(.*)</body>", html_source, re.DOTALL | re.IGNORECASE)
    if body_match:
        return body_match.group(1).strip()
    return html_source.strip()


def ready_script(slug: str) -> str:
    escaped = json.dumps(slug)
    return f"""
<script>
(() => {{
  async function markReady() {{
    try {{
      if (document.fonts && document.fonts.ready) {{
        await document.fonts.ready;
      }}
    }} catch (_error) {{
      // Ignore font readiness failures and continue with the rendered fallback.
    }}

    await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));

    document.documentElement.dataset.previewReady = '1';
    document.body && (document.body.dataset.previewReady = '1');

    if (window.parent !== window) {{
      window.parent.postMessage({{ type: 'blog-figure-preview-ready', slug: {escaped} }}, '*');
    }}
  }}

  if (document.readyState === 'complete') {{
    markReady();
  }} else {{
    window.addEventListener('load', markReady, {{ once: true }});
  }}
}})();
</script>
""".strip()


def render_document(pattern: Pattern, skill_dir: Path) -> str:
    skill_dir_uri = skill_dir.resolve().as_uri()
    source = pattern.html.replace(f"file://{{SKILL_DIR}}/assets/figure.css", PREVIEW_CSS_PATH)
    source = source.replace("{SKILL_DIR}", skill_dir_uri)
    ready = ready_script(pattern.slug)

    if re.search(r"<!DOCTYPE html>|<html\b", source, re.IGNORECASE):
        if "</body>" in source:
            return source.replace("</body>", f"{ready}\n</body>")
        return f"{source}\n{ready}\n"

    body = extract_body(source)
    title = html.escape(f"{pattern.number:02d}. {pattern.name}")
    return f"""<!DOCTYPE html>
<html lang="ko" data-preview-ready="0">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=1440">
  <title>{title}</title>
  <link rel="stylesheet" href="{PREVIEW_CSS_PATH}">
</head>
<body data-pattern-slug="{pattern.slug}" data-preview-ready="0">
{body}
{ready}
</body>
</html>
"""


def render_index(patterns: list[Pattern]) -> str:
    cards = []
    for pattern in patterns:
        card = f"""
      <article class="card" data-slug="{pattern.slug}">
        <div class="thumb">
          <iframe
            loading="eager"
            referrerpolicy="no-referrer"
            src="./{pattern.slug}.html"
            title="{html.escape(pattern.name)}"
          ></iframe>
        </div>
        <div class="meta">
          <div class="eyebrow">{pattern.number:02d} · {html.escape(pattern.category)}</div>
          <a href="./{pattern.slug}.html" target="_blank" rel="noreferrer">{html.escape(pattern.name)}</a>
          <div class="source">{html.escape(pattern.source_file)}</div>
        </div>
      </article>
""".rstrip()
        cards.append(card)

    cards_html = "\n".join(cards)
    total = len(patterns)
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Blog Figure Pattern Gallery</title>
  <style>
    :root {{
      color-scheme: light;
      --bg: #f5f5f5;
      --card: #ffffff;
      --line: #0a0a0a;
      --muted: #616161;
      --accent: #0968F6;
      --success: #288034;
      --shadow: 6px 6px 0px var(--line);
    }}

    * {{ box-sizing: border-box; }}

    body {{
      margin: 0;
      min-width: 1600px;
      font-family: "SF Pro Text", "Noto Sans KR", sans-serif;
      background: var(--bg);
      color: var(--line);
    }}

    .page {{
      padding: 32px 32px 56px;
    }}

    .header {{
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      gap: 24px;
      margin-bottom: 24px;
    }}

    .title {{
      margin: 0;
      font-size: 40px;
      line-height: 1.05;
      font-weight: 900;
    }}

    .subtitle {{
      margin: 10px 0 0;
      max-width: 720px;
      font-size: 18px;
      line-height: 1.45;
      color: var(--muted);
    }}

    .status {{
      flex: none;
      min-width: 220px;
      padding: 16px 18px;
      border: 3px solid var(--line);
      background: var(--card);
      box-shadow: var(--shadow);
      text-align: right;
    }}

    .status-label {{
      display: block;
      font-size: 13px;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--muted);
    }}

    #ready-count {{
      display: block;
      margin-top: 8px;
      font-size: 28px;
      font-weight: 900;
    }}

    .status-stack {{
      display: grid;
      gap: 14px;
      justify-items: end;
    }}

    .density-controls {{
      display: inline-flex;
      gap: 8px;
      align-items: center;
      justify-content: flex-end;
    }}

    .density-controls button {{
      border: 3px solid var(--line);
      background: var(--card);
      color: var(--line);
      font: inherit;
      font-size: 14px;
      font-weight: 800;
      padding: 10px 14px;
      cursor: pointer;
      box-shadow: 4px 4px 0px var(--line);
    }}

    .density-controls button[aria-pressed="true"] {{
      background: var(--accent);
      color: white;
    }}

    .grid {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 24px;
    }}

    .card {{
      border: 3px solid var(--line);
      background: var(--card);
      box-shadow: var(--shadow);
      padding: 14px;
      transition: transform 120ms ease, box-shadow 120ms ease;
    }}

    .card[data-ready="1"] {{
      box-shadow: 8px 8px 0px var(--success);
    }}

    .thumb {{
      width: 100%;
      aspect-ratio: 16 / 9;
      overflow: hidden;
      border: 3px solid var(--line);
      background: #e5e5e5;
    }}

    iframe {{
      width: 1440px;
      height: 810px;
      border: 0;
      transform-origin: top left;
      transform: scale(0.25);
      pointer-events: none;
      background: #f5f5f5;
    }}

    .page[data-density="detail"] .grid {{
      grid-template-columns: repeat(2, minmax(0, 1fr));
    }}

    .page[data-density="detail"] .thumb {{
      aspect-ratio: 16 / 10;
    }}

    .page[data-density="detail"] iframe {{
      transform: scale(0.4);
    }}

    .meta {{
      display: grid;
      gap: 6px;
      margin-top: 12px;
    }}

    .eyebrow {{
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      color: var(--muted);
    }}

    .meta a {{
      color: var(--line);
      font-size: 24px;
      font-weight: 900;
      text-decoration: none;
    }}

    .source {{
      font-size: 14px;
      color: var(--muted);
    }}
  </style>
</head>
<body data-gallery-ready="0">
  <main class="page" data-density="detail">
    <header class="header">
      <div>
        <h1 class="title">Blog Figure Pattern Gallery</h1>
        <p class="subtitle">
          Render all {total} canonical examples from the reference markdown. Wait for the ready counter
          before taking screenshots in DevTools or Playwright. Use `Detail` mode when checking label
          collisions, clipping, and whitespace balance.
        </p>
      </div>
      <div class="status-stack">
        <div class="density-controls" role="group" aria-label="Gallery density">
          <button type="button" data-density="compact" aria-pressed="false">Compact</button>
          <button type="button" data-density="detail" aria-pressed="true">Detail</button>
        </div>
        <div class="status">
          <span class="status-label">Previews Ready</span>
          <span id="ready-count">0 / {total} ready</span>
        </div>
      </div>
    </header>

    <section class="grid">
{cards_html}
    </section>
  </main>

  <script>
    const total = {total};
    const ready = new Set();
    const counter = document.getElementById('ready-count');
    const page = document.querySelector('.page');
    const densityButtons = Array.from(document.querySelectorAll('.density-controls button'));

    function applyDensity(nextDensity, persist = true) {{
      const density = nextDensity === 'detail' ? 'detail' : 'compact';
      page.dataset.density = density;
      densityButtons.forEach(button => {{
        button.setAttribute('aria-pressed', button.dataset.density === density ? 'true' : 'false');
      }});
      const params = new URLSearchParams(window.location.search);
      params.set('density', density);
      history.replaceState(null, '', `${{window.location.pathname}}?${{params.toString()}}`);
      if (persist) {{
        window.localStorage.setItem('blog-figure-preview-density', density);
      }}
    }}

    function updateCount() {{
      counter.textContent = `${{ready.size}} / ${{total}} ready`;
      document.body.dataset.galleryReady = ready.size === total ? '1' : '0';
    }}

    window.addEventListener('message', event => {{
      if (!event.data || event.data.type !== 'blog-figure-preview-ready') return;
      ready.add(event.data.slug);
      const card = document.querySelector(`.card[data-slug="${{event.data.slug}}"]`);
      if (card) card.dataset.ready = '1';
      updateCount();
    }});

    document.querySelectorAll('.card iframe').forEach(frame => {{
      frame.addEventListener('load', () => {{
        const slug = frame.closest('.card')?.dataset.slug;
        if (!slug) return;
        window.setTimeout(() => {{
          if (ready.has(slug)) return;
          ready.add(slug);
          frame.closest('.card')?.setAttribute('data-ready', '1');
          updateCount();
        }}, 800);
      }});
    }});

    densityButtons.forEach(button => {{
      button.addEventListener('click', () => applyDensity(button.dataset.density));
    }});

    const params = new URLSearchParams(window.location.search);
    applyDensity(
      params.get('density') || window.localStorage.getItem('blog-figure-preview-density') || 'detail',
      false
    );
  </script>
</body>
</html>
"""


def write_outputs(patterns: list[Pattern], output_dir: Path, skill_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    assets_dir = output_dir / "_assets"
    assets_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(skill_dir / "assets" / "figure.css", assets_dir / "figure.css")

    manifest = []
    for pattern in patterns:
      (output_dir / f"{pattern.slug}.html").write_text(
          render_document(pattern, skill_dir), encoding="utf-8"
      )
      manifest.append(asdict(pattern))

    (output_dir / "index.html").write_text(render_index(patterns), encoding="utf-8")
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        default="/tmp/blog-figure-previews",
        help="Directory for generated previews (default: %(default)s)",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Delete the output directory before writing new files",
    )
    args = parser.parse_args()

    skill_dir = Path(__file__).resolve().parent.parent
    output_dir = Path(args.output_dir).expanduser().resolve()

    if args.clean and output_dir.exists():
        shutil.rmtree(output_dir)

    patterns = parse_patterns(skill_dir)
    if len(patterns) != 30:
        raise SystemExit(f"Expected 30 patterns, found {len(patterns)}")

    write_outputs(patterns, output_dir, skill_dir)
    print(f"Rendered {len(patterns)} patterns into {output_dir}")
    print(f"Gallery: {output_dir / 'index.html'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
