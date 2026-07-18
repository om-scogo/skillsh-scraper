#!/usr/bin/env python3
"""Static linter for blog-figure HTML against design-rules.md.

The figure HTML an agent writes is the *only* place design-rule violations
creep in — figure.css is already compliant and linked externally. This script
reads the standalone HTML (inline styles, <style> blocks, SVG attributes, and
<script> for canvas/D3) and flags the rules that are objectively checkable, so
the agent self-corrects *before* spending a browser capture and showing the user
a figure that's unreadable at 25% mobile scale.

It does NOT render anything. Pair it with the capture step: lint first, capture
only once the lint is clean.

Usage:
    python3 validate_figure.py /tmp/blog-figure-foo.html
    python3 validate_figure.py /tmp/blog-figure-foo.html --pattern Terminal
    python3 validate_figure.py /tmp/blog-figure-foo.html --json

Exit code 0 = no ERRORs (WARNINGs allowed). Non-zero = at least one ERROR.
"""
from __future__ import annotations

import argparse
import json
import re
import sys

# --- word budget per design-rules.md ("Figure 전체: max 20단어, Terminal 35") ---
WORD_BUDGET_DEFAULT = 20
WORD_BUDGET_TERMINAL = 35

# --- per-pattern component caps (design-rules.md "컴포넌트 수량 제한" table) ---
# class substring -> (max count, human label). Heuristic: counts occurrences of a
# per-item class in the HTML. Keyed on the class that appears exactly once per
# capped unit (e.g. slope-line = one <line> per item), so the count maps cleanly
# to the documented cap and false positives stay rare.
#
# Intentionally omitted (documented caps with no reliable static selector — per
# the SKILL guidance, don't force a count that's ambiguous):
#   - Waffle: the 10×10 grid legitimately has 100 `.waffle-cell` rects; the "2
#     카테고리" cap is on the legend, which has no class. Capping the cells would
#     false-positive on every valid waffle.
#   - Sparkline Grid: cards are generated in <script> from a JS array — no static
#     class markup to count.
#   - Waterfall: bars share a bare `.bar` class, and `\bbar\b` also matches the
#     Data Viz `bar-fill`/`bar-row`/… tokens (hyphen is a word boundary), so a cap
#     on `bar` would misfire on bar charts.
COMPONENT_CAPS = {
    "flow-card": (3, "Flow 단계"),
    "tl-block": (3, "Timeline 블록"),
    "story-panel": (4, "Storyboard 패널"),
    "bar-row": (4, "Bar chart 행"),
    "journey-step": (4, "Journey 단계"),
    "loop-node": (4, "Loop 노드"),
    "arch-layer": (3, "Architecture 레이어"),
    "terminal-card": (3, "Terminal 카드"),
    "matrix-cell": (4, "Matrix 셀 (2×2)"),
    "slope-line": (5, "Slope 항목"),
    "db-line": (5, "Dumbbell 행"),
    "actual": (4, "Bullet 차트"),
}

# Valid CSS hex color (3/4/6/8 digits). Skip HTML entities (&#10095;) via the
# `&` lookbehind, and avoid matching a longer hex run via the trailing guard.
HEX_RE = re.compile(r"(?<!&)#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{4}|[0-9a-fA-F]{3})(?![0-9a-fA-F])")
FONT_PX_RE = re.compile(r"font-size\s*:\s*([0-9.]+)px", re.I)
FONT_REM_RE = re.compile(r"font-size\s*:\s*([0-9.]+)rem", re.I)
# SVG font-size attribute (font-size="24" | "24px" | "1.5rem"). Captures the unit
# so rem/em can be converted to px (×16) before the <20px comparison; unitless == px.
SVG_FONT_RE = re.compile(r'font-size\s*=\s*["\']?\s*([0-9.]+)\s*(px|rem|em)?', re.I)
SCRIPT_RE = re.compile(r"<script\b[^>]*>.*?</script>", re.I | re.S)
STYLE_BLOCK_RE = re.compile(r"<style\b[^>]*>.*?</style>", re.I | re.S)
SVG_BLOCK_RE = re.compile(r"<svg\b.*?</svg>", re.I | re.S)
SVG_TAG_RE = re.compile(r"<svg\b", re.I)
CANVAS_TAG_RE = re.compile(r"<canvas\b", re.I)
# CSS custom-property definition (`--token: #hex`). The one place a hex literal
# legitimately lives when figure.css var(--*) is the rule, so it's exempt from the
# hex check even in a plain <style> block.
CUSTOM_PROP_DECL_RE = re.compile(r"--[\w-]+\s*:\s*[^;{}]*")
TAG_RE = re.compile(r"<[^>]+>")
WORD_RE = re.compile(r"[A-Za-z0-9]+|[가-힣]+")  # latin runs + hangul runs


def line_of(text: str, idx: int) -> int:
    return text.count("\n", 0, idx) + 1


def _blank_block(regex: re.Pattern, html: str) -> str:
    """Replace matched blocks with blank lines (preserve line numbers)."""
    return regex.sub(lambda m: "\n" * m.group(0).count("\n"), html)


def strip_scripts(html: str) -> str:
    return _blank_block(SCRIPT_RE, html)


def check_hex_colors(html: str, findings: list) -> None:
    """Hardcoded hex is banned in HTML/CSS layout context (use var(--*)).

    Generative graphics legitimately use hex — the reference patterns set hex
    fills inside <svg>, <canvas>/<script>, and the <style> blocks that drive
    them. Scripts and <svg> blocks are always blanked out. The <style> block is
    where it gets nuanced:

    - If the figure has any <svg>/<canvas>, its <style> may be setting fills that
      drive that generative graphic, so skip the whole <style> (avoids false
      positives on generative patterns) — the original behavior.
    - If there is NO <svg>/<canvas>, it's a pure layout figure: a <style> block
      must use figure.css var(--*), so scan it too. Only CSS custom-property
      definitions (`:root { --token: #hex }`) legitimately hold a hex literal, so
      blank just those and flag every other hardcoded hex.
    """
    has_graphics = bool(SVG_TAG_RE.search(html) or CANVAS_TAG_RE.search(html))
    scannable = _blank_block(SCRIPT_RE, html)
    scannable = _blank_block(SVG_BLOCK_RE, scannable)
    if has_graphics:
        scannable = _blank_block(STYLE_BLOCK_RE, scannable)
    else:
        scannable = _blank_block(CUSTOM_PROP_DECL_RE, scannable)
    for m in HEX_RE.finditer(scannable):
        ln = line_of(scannable, m.start())
        findings.append((
            "ERROR", "hex-color", ln,
            f"하드코딩 hex '{m.group(0)}' — figure.css의 var(--*) 변수를 쓰세요 "
            f"(SVG/Canvas/D3 그래픽 내부는 예외).",
        ))


def check_gradients(html: str, findings: list) -> None:
    patterns = [
        (r"linear-gradient", "CSS linear-gradient"),
        (r"radial-gradient", "CSS radial-gradient"),
        (r"conic-gradient", "CSS conic-gradient"),
        (r"<linearGradient", "SVG <linearGradient>"),
        (r"<radialGradient", "SVG <radialGradient>"),
        (r"createLinearGradient", "Canvas createLinearGradient"),
        (r"createRadialGradient", "Canvas createRadialGradient"),
    ]
    for pat, label in patterns:
        for m in re.finditer(pat, html, re.I):
            ln = line_of(html, m.start())
            findings.append((
                "ERROR", "gradient", ln,
                f"{label} 발견 — Neo-Brutalism은 평면 단색만. 그라데이션 금지.",
            ))


def _blur_token(shadow: str) -> float | None:
    """Return the blur radius (3rd length) of a single box/text-shadow, or None
    if it can't be parsed (e.g. uses var())."""
    if "var(" in shadow:
        return None
    lengths = re.findall(r"(-?[0-9.]+)(?:px|rem|em)\b|(?<![\w.])(0)(?![\w.])", shadow)
    nums = [a or b for (a, b) in lengths]
    if len(nums) >= 3:
        try:
            return abs(float(nums[2]))
        except ValueError:
            return None
    return None


def check_blur(html: str, findings: list) -> None:
    # box-shadow / text-shadow with non-zero blur
    for prop in ("box-shadow", "text-shadow"):
        for m in re.finditer(prop + r"\s*:\s*([^;\"'}]+)", html, re.I):
            value = m.group(1)
            ln = line_of(html, m.start())
            for shadow in value.split(","):
                blur = _blur_token(shadow)
                if blur is not None and blur > 0:
                    findings.append((
                        "ERROR", "blur-shadow", ln,
                        f"{prop} blur={blur:g} — 그림자는 'Npx Npx 0px'(blur 0)만 허용.",
                    ))
    # filter: blur(...) and svg feGaussianBlur / drop-shadow
    for pat, label in [
        (r"filter\s*:\s*blur", "filter: blur"),
        (r"backdrop-filter\s*:\s*blur", "backdrop-filter: blur"),
        (r"drop-shadow", "drop-shadow"),
        (r"feGaussianBlur", "SVG feGaussianBlur"),
    ]:
        for m in re.finditer(pat, html, re.I):
            ln = line_of(html, m.start())
            findings.append((
                "ERROR", "blur-shadow", ln, f"{label} 발견 — 소프트 엣지/블러 금지.",
            ))


def check_fonts(html_no_script: str, findings: list) -> None:
    # CSS px
    for m in FONT_PX_RE.finditer(html_no_script):
        size = float(m.group(1))
        if size < 20:
            ln = line_of(html_no_script, m.start())
            findings.append((
                "ERROR", "small-font", ln,
                f"font-size:{size:g}px < 20px — 모바일 25% 축소 시 안 보임 "
                f"(콘텐츠는 24px 이상 권장).",
            ))
    # CSS rem
    for m in FONT_REM_RE.finditer(html_no_script):
        rem = float(m.group(1))
        if rem < 1.25:
            ln = line_of(html_no_script, m.start())
            findings.append((
                "ERROR", "small-font", ln,
                f"font-size:{rem:g}rem < 1.25rem(20px) — 최소 폰트 위반.",
            ))
    # SVG font-size="N" (unitless == px; rem/em == 16px). Only inside <svg> blocks.
    for svg in re.finditer(r"<svg\b.*?</svg>", html_no_script, re.I | re.S):
        block = svg.group(0)
        base = svg.start()
        for m in SVG_FONT_RE.finditer(block):
            raw = float(m.group(1))
            unit = (m.group(2) or "").lower()
            px = raw * 16 if unit in ("rem", "em") else raw
            if px < 20:
                ln = line_of(html_no_script, base + m.start())
                shown = f"{m.group(1)}{unit}" if unit else m.group(1)
                findings.append((
                    "ERROR", "small-font", ln,
                    f"SVG font-size={shown} ({px:g}px) < 20 — 18px 이하 금지.",
                ))


def visible_text(html: str) -> str:
    no_script = SCRIPT_RE.sub(" ", html)
    no_style = STYLE_BLOCK_RE.sub(" ", no_script)
    return TAG_RE.sub(" ", no_style)


def check_word_count(html: str, budget: int, findings: list) -> None:
    text = visible_text(html)
    words = WORD_RE.findall(text)
    n = len(words)
    if n > budget:
        findings.append((
            "WARNING", "word-count", 0,
            f"본문 텍스트 약 {n}단어 > {budget}단어 한도 — Figure는 글 요약이 아니라 "
            f"시각 앵커. 명사구로 줄이세요. (SVG 텍스트 포함, Canvas/D3 라벨 제외 근사치)",
        ))


def check_component_caps(html: str, findings: list) -> None:
    for cls, (cap, label) in COMPONENT_CAPS.items():
        n = len(re.findall(r'class\s*=\s*["\'][^"\']*\b' + re.escape(cls) + r'\b', html))
        if n > cap:
            findings.append((
                "WARNING", "component-cap", 0,
                f"{label} {n}개 > 최대 {cap}개 — 적은 수의 큰 컴포넌트가 더 잘 읽힙니다.",
            ))


def check_provenance(html: str, findings: list) -> None:
    """SKILL.md HTML Template의 provenance 주석(blog/scene/pattern) 존재 확인.

    없어도 렌더링에는 무해하므로 WARNING — 단 다음 세션이 이 figure를 재수정할 때
    어느 블로그의 어떤 장면인지 추적할 수 없게 된다."""
    if "blog-figure source" not in html[:4096]:
        findings.append((
            "WARNING", "provenance", 0,
            "provenance 주석(<!-- blog-figure source ... -->)이 없습니다 — "
            "다음 세션에서 이 figure의 출처(블로그/장면/패턴)를 추적할 수 없습니다.",
        ))


def check_structure(html: str, findings: list) -> None:
    if "figure.css" not in html:
        findings.append((
            "WARNING", "css-link", 0,
            "figure.css 링크가 없습니다 — 스타일이 빠져 무미한 figure가 됩니다.",
        ))
    has_viewport = re.search(r'name=["\']viewport["\'][^>]*width=1440', html, re.I)
    has_viewbox = re.search(r'viewBox=["\']0 0 1440 810', html)
    if not has_viewport and not has_viewbox:
        findings.append((
            "WARNING", "canvas-size", 0,
            "viewport width=1440 또는 SVG viewBox '0 0 1440 810'이 없습니다 — "
            "16:9 캔버스 크기를 확인하세요.",
        ))


def validate(html: str, pattern: str | None) -> list:
    findings: list = []
    html_no_script = strip_scripts(html)
    check_hex_colors(html, findings)
    check_gradients(html, findings)
    check_blur(html, findings)
    check_fonts(html_no_script, findings)
    budget = WORD_BUDGET_TERMINAL if (pattern or "").lower() == "terminal" else WORD_BUDGET_DEFAULT
    check_word_count(html, budget, findings)
    check_component_caps(html, findings)
    check_provenance(html, findings)
    check_structure(html, findings)
    findings.sort(key=lambda f: (f[0] != "ERROR", f[2]))
    return findings


def main() -> int:
    ap = argparse.ArgumentParser(description="Lint blog-figure HTML against design rules.")
    ap.add_argument("html", help="path to the figure HTML file")
    ap.add_argument("--pattern", default=None, help="pattern name (raises word budget for Terminal)")
    ap.add_argument("--json", action="store_true", help="emit JSON instead of text")
    args = ap.parse_args()

    try:
        with open(args.html, encoding="utf-8") as fh:
            html = fh.read()
    except OSError as exc:
        print(f"cannot read {args.html}: {exc}", file=sys.stderr)
        return 2

    findings = validate(html, args.pattern)
    errors = [f for f in findings if f[0] == "ERROR"]
    warnings = [f for f in findings if f[0] == "WARNING"]

    if args.json:
        print(json.dumps({
            "file": args.html,
            "pattern": args.pattern,
            "ok": not errors,
            "error_count": len(errors),
            "warning_count": len(warnings),
            "findings": [
                {"severity": s, "rule": r, "line": ln, "message": msg}
                for (s, r, ln, msg) in findings
            ],
        }, ensure_ascii=False, indent=2))
        return 1 if errors else 0

    if not findings:
        print(f"✅ {args.html}: 모든 디자인 룰 통과.")
        return 0

    for sev, rule, ln, msg in findings:
        loc = f"line {ln}" if ln else "file"
        mark = "❌" if sev == "ERROR" else "⚠️ "
        print(f"{mark} [{rule}] {loc}: {msg}")

    print()
    print(f"{len(errors)} error, {len(warnings)} warning.")
    if errors:
        print("→ ERROR를 모두 고친 뒤 캡처하세요. (이미 캡처했다면 HTML 수정 후 재캡처)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
