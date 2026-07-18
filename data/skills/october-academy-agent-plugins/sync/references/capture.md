# Capture Reference

Figure HTML을 1440×810 retina 2x PNG로 캡처하는 절차. SKILL.md Workflow 6단계(캡처)에서 읽어라.
도구 우선순위: **Chrome DevTools MCP → Chrome CLI(retina 2x) → Playwright MCP/CLI(1x, 최후 수단)**.

## 캡처 전 폰트 로드 확인 (필수)

`document.fonts.check()`로 검사하지 마라 — Google Fonts CSS 로드 자체가 실패하면(@font-face
미등록) `check()`는 매칭 face가 없어도 true를 반환하므로, 정확히 그 실패 모드(오프라인·CDN
차단)를 통과시킨다. 대신 페이지 컨텍스트에서 로드된 face의 존재를 직접 단언하라:

```js
await document.fonts.ready;
const noto = [...document.fonts].filter(f => f.family.replace(/["']/g, '') === 'Noto Sans KR');
const ok = noto.some(f => f.status === 'loaded') && !noto.some(f => f.status === 'error');
```

`ok`가 false면 시스템 fallback 폰트로 그대로 캡처하지 말고, 네트워크 상태를 점검한 뒤 재시도하라.
문서가 실제로 쓰는 weight(본문 700, 타이틀 900)는 사용 시점에 로드가 트리거되므로 실패하면
`status === 'error'`로 잡힌다. `validate_figure.py`는 정적 린트일 뿐이라 폰트 렌더링 깨짐은 잡지
못한다 — 이건 육안 확인의 몫이다.

## 30개 패턴 전체 검수용 gallery

```bash
python3 {SKILL_DIR}/scripts/render_pattern_previews.py --clean --output-dir /tmp/blog-figure-previews
```

검수용 gallery는 `file:///tmp/blog-figure-previews/index.html` 이다. Playwright MCP/CLI는 `file://`를 차단할 수 있으니 필요하면 `python3 -m http.server 8123 --directory /private/tmp` 후 `http://127.0.0.1:8123/blog-figure-previews/index.html`로 연다. 상세 검수는 `?density=detail` 쿼리를 붙여 2열 확대 모드로 본다. 상단 ready counter가 `30 / 30 ready`가 된 뒤 캡처하라.

## Chrome DevTools MCP (preferred when Chrome is open)

1. `mcp__chrome-devtools__emulate` → viewport `{width:1440, height:810, deviceScaleFactor:2}` (retina 2880×1620)
2. `mcp__chrome-devtools__navigate_page` → `file:///tmp/blog-figure-{name}.html`
3. `mcp__chrome-devtools__take_screenshot` → `filePath: {target}.png`
4. After capture: `mcp__chrome-devtools__emulate` → viewport `null` (reset)

## Chrome CLI (retina 2x 가능 — Chrome DevTools MCP 다음 순위)

macOS 바이너리: `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`

```bash
# 단일 figure — retina 2x (2880×1620)
google-chrome --headless --disable-gpu --hide-scrollbars --force-device-scale-factor=2 --virtual-time-budget=5000 --window-size=1440,810 --screenshot={target}.png "file:///tmp/blog-figure-{name}.html"
# 30-pattern gallery 검수
google-chrome --headless --disable-gpu --hide-scrollbars --virtual-time-budget=5000 --window-size=1600,4200 --screenshot=/tmp/blog-figure-previews/gallery-chrome.png "file:///tmp/blog-figure-previews/index.html?density=detail"
```

**hang 주의 — blocking 실행 금지**: headless Chrome이 스크린샷을 저장한 뒤에도 프로세스가
종료되지 않는 경우가 있다(연속 캡처 중 실측 — 2번째 호출에서 2분 타임아웃). 셸에서 순차
blocking으로 돌리지 말고, 백그라운드로 띄운 뒤 **PNG 파일 생성(>5KB)을 폴링하고 terminate**하라:

```python
import subprocess, time
from pathlib import Path
out = Path("{target}.png")
p = subprocess.Popen([CHROME, ...flags..., f"--screenshot={out}", f"file://{html}"])
t0 = time.time()
while time.time() - t0 < 35:
    if out.exists() and out.stat().st_size > 5000: time.sleep(1.2); break
    time.sleep(0.3)
if p.poll() is None: p.terminate()
```

연속 캡처 시 `--user-data-dir`도 figure마다 분리하면 프로필 락 간섭까지 차단된다.

## Playwright MCP (deviceScaleFactor 지정 불가 → 1440×810 1x 산출. 최후 수단)

1. `mcp__playwright__browser_resize` → 1440×810
2. `mcp__playwright__browser_navigate` → `file:///tmp/blog-figure-{name}.html`
3. `mcp__playwright__browser_take_screenshot` → `filename: {target}.png`

## Playwright CLI (`--scale`/`--device-scale-factor` 플래그 부재 → 1440×810 1x 산출. 최후 수단)

```bash
npx playwright screenshot --viewport-size="1440,810" file:///tmp/blog-figure-{name}.html {target}.png
npx playwright screenshot --viewport-size="1600,4200" --wait-for-selector="body[data-gallery-ready='1']" --wait-for-timeout=3000 "http://127.0.0.1:8123/blog-figure-previews/index.html?density=detail" /tmp/blog-figure-previews/gallery-playwright.png
```

## 캡처 실패 시 복구

1. Chrome DevTools 연결 실패 → Chrome CLI(retina 2x) 시도 → Playwright MCP/CLI(1x, 최후 수단) 시도
2. 빈 PNG / 흰 화면 → HTML 파일을 `Read`로 확인 후 `file://` 경로가 올바른지 점검. `{SKILL_DIR}` 경로가 실제 figure.css 위치와 일치하는지 확인
3. 폰트 깨짐 → Canvas/D3 패턴에서 `document.fonts.ready.then()` 래핑 누락 여부 확인
4. 모든 방법 실패 → HTML 파일 경로를 사용자에게 알려주고 수동 캡처 요청
