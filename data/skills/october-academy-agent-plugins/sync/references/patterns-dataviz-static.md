# Figure Patterns — Data Visualization (Static)

CSS/SVG-static patterns (no JS): Data Viz, Waffle, Slope, Dumbbell, Bullet, Waterfall.

All use `assets/figure.css`. **핵심 원칙**:
- 텍스트는 최소화하되 **직접 라벨**을 우선한다.
- small multiple 비교는 **shared scale**을 기본값으로 둔다.
- 범례는 꼭 필요할 때만 쓰고, 가능하면 **차트 안에서 설명**한다.
- Radar는 **동일 스케일 축 5개 이하 / 시리즈 2개 이하**일 때만 사용한다.
- 모바일 25% 축소에서도 구조가 남도록, 색보다 **정렬·여백·두께**로 위계를 만든다.

## TOC

- 14. Data Viz
- 21. Waffle
- 23. Slope
- 26. Dumbbell
- 28. Bullet
- 30. Waterfall

---

## 14. Data Viz (데이터 시각화)

Best for: 수치 비교, 비율, 설문 결과, 벤치마크

Key classes: `.bar-chart`, `.bar-row`, `.bar-label`, `.bar-track`, `.bar-fill`, `.bar-value`

Max: **4행**

```html
<body>
  <div class="bar-chart" style="gap:2.5rem">
    <div class="bar-row">
      <div class="bar-label">React</div>
      <div class="bar-track" style="height:104px"><div class="bar-fill" style="width:85%;background:var(--dark);color:var(--white)">85%</div></div>
    </div>
    <div class="bar-row">
      <div class="bar-label">Vue</div>
      <div class="bar-track" style="height:104px"><div class="bar-fill" style="width:78%;background:var(--dark);color:var(--white)">78%</div></div>
    </div>
    <div class="bar-row">
      <div class="bar-label">Svelte</div>
      <div class="bar-track" style="height:104px"><div class="bar-fill" style="width:92%;background:var(--accent);color:var(--white)">92%</div></div>
    </div>
    <div class="bar-row">
      <div class="bar-label">Angular</div>
      <div class="bar-track" style="height:104px"><div class="bar-fill" style="width:54%;background:var(--dark);color:var(--white)">54%</div></div>
    </div>
  </div>
</body>
```

Notes: `width` 퍼센트로 바 길이 설정. 라벨은 단어 1~2개. `body`가 세로 중앙 정렬하므로, 4행이 810 캔버스를 균형 있게 채우도록 `bar-track` 높이(104px)와 `bar-chart` gap(2.5rem)을 인라인으로 키웠다 — 적은 수의 큰 바가 25% 축소에서도 잘 읽힌다. **바 색은 단색(`--dark`) + 강조 1색(`--accent`)이 기본** — 행(위치)이 이미 항목을 구분하므로 바마다 다른 hue를 입히면 색이 가짜 범주를 만든다(색은 인코딩 수단). 색은 "어느 바를 봐야 하는가"에만 쓴다. **예외 — 같은 항목은 패턴을 넘어 같은 색**: 같은 블로그에서 Slope·Treemap·Sparkline 등 다색 패턴과 세트로 쓰여 항목-색 매핑이 이미 성립했다면, 세트 일관성이 단색 원칙보다 우선한다.

---

## 21. Waffle (SVG 인라인)

Best for: 비율 체감, 퍼센트 시각화, 100칸 중 N칸으로 비율을 직관적으로 표현

Approach: **SVG inline** — 10x10 `<rect>` 그리드 (100개 셀). 셀 52x52, gap 4px.

Max: **2 카테고리**, 총 ~8단어 (범례 포함)

```html
<body>
<svg viewBox="0 0 1440 810" xmlns="http://www.w3.org/2000/svg"
     style="width:1440px;height:810px;background:#f5f5f5">
  <defs>
    <style>
      text { font-family: 'Noto Sans KR', sans-serif; fill: #0a0a0a; }
      .waffle-cell { stroke: #0a0a0a; stroke-width: 2.5; }
    </style>
    <pattern id="dots" width="16" height="16" patternUnits="userSpaceOnUse">
      <circle cx="8" cy="8" r="1" fill="rgba(10,10,10,0.06)"/>
    </pattern>
  </defs>
  <rect width="1440" height="810" fill="url(#dots)"/>

  <!-- Waffle grid: 10x10 = 100 cells, 72 filled (#0968F6), 28 empty (#e5e5e5) -->
  <!-- Grid generation rule (전체 100칸을 실제로 렌더):
       - 10 rows (row 0-9), 10 cols (col 0-9)
       - Cell origin: x = 280 + col * 56, y = 127 + row * 56
       - Cell size: width="52" height="52", class="waffle-cell" (gap 4px)
       - Fill order: left-to-right, top-to-bottom (cell index = row*10 + col)
       - Cells 0-71 (first 72): fill="#0968F6" (filled/active)
       - Cells 72-99 (remaining 28): fill="#e5e5e5" (empty/inactive)
       - So rows 0-6 are all #0968F6 (70 cells)
       - Row 7 (y=519): cols 0-1 #0968F6 (last 2 filled), cols 2-9 #e5e5e5
       - Rows 8-9: all #e5e5e5
       - Grid spans x 280-836, y 127-683 (810 캔버스에 수직 중앙) -->
  <rect class="waffle-cell" x="280" y="127" width="52" height="52" fill="#0968F6"/>
  <rect class="waffle-cell" x="336" y="127" width="52" height="52" fill="#0968F6"/>
  <rect class="waffle-cell" x="392" y="127" width="52" height="52" fill="#0968F6"/>
  <rect class="waffle-cell" x="448" y="127" width="52" height="52" fill="#0968F6"/>
  <rect class="waffle-cell" x="504" y="127" width="52" height="52" fill="#0968F6"/>
  <rect class="waffle-cell" x="560" y="127" width="52" height="52" fill="#0968F6"/>
  <rect class="waffle-cell" x="616" y="127" width="52" height="52" fill="#0968F6"/>
  <rect class="waffle-cell" x="672" y="127" width="52" height="52" fill="#0968F6"/>
  <rect class="waffle-cell" x="728" y="127" width="52" height="52" fill="#0968F6"/>
  <rect class="waffle-cell" x="784" y="127" width="52" height="52" fill="#0968F6"/>

  <rect class="waffle-cell" x="280" y="183" width="52" height="52" fill="#0968F6"/>
  <rect class="waffle-cell" x="336" y="183" width="52" height="52" fill="#0968F6"/>
  <rect class="waffle-cell" x="392" y="183" width="52" height="52" fill="#0968F6"/>
  <rect class="waffle-cell" x="448" y="183" width="52" height="52" fill="#0968F6"/>
  <rect class="waffle-cell" x="504" y="183" width="52" height="52" fill="#0968F6"/>
  <rect class="waffle-cell" x="560" y="183" width="52" height="52" fill="#0968F6"/>
  <rect class="waffle-cell" x="616" y="183" width="52" height="52" fill="#0968F6"/>
  <rect class="waffle-cell" x="672" y="183" width="52" height="52" fill="#0968F6"/>
  <rect class="waffle-cell" x="728" y="183" width="52" height="52" fill="#0968F6"/>
  <rect class="waffle-cell" x="784" y="183" width="52" height="52" fill="#0968F6"/>

  <rect class="waffle-cell" x="280" y="239" width="52" height="52" fill="#0968F6"/>
  <rect class="waffle-cell" x="336" y="239" width="52" height="52" fill="#0968F6"/>
  <rect class="waffle-cell" x="392" y="239" width="52" height="52" fill="#0968F6"/>
  <rect class="waffle-cell" x="448" y="239" width="52" height="52" fill="#0968F6"/>
  <rect class="waffle-cell" x="504" y="239" width="52" height="52" fill="#0968F6"/>
  <rect class="waffle-cell" x="560" y="239" width="52" height="52" fill="#0968F6"/>
  <rect class="waffle-cell" x="616" y="239" width="52" height="52" fill="#0968F6"/>
  <rect class="waffle-cell" x="672" y="239" width="52" height="52" fill="#0968F6"/>
  <rect class="waffle-cell" x="728" y="239" width="52" height="52" fill="#0968F6"/>
  <rect class="waffle-cell" x="784" y="239" width="52" height="52" fill="#0968F6"/>

  <rect class="waffle-cell" x="280" y="295" width="52" height="52" fill="#0968F6"/>
  <rect class="waffle-cell" x="336" y="295" width="52" height="52" fill="#0968F6"/>
  <rect class="waffle-cell" x="392" y="295" width="52" height="52" fill="#0968F6"/>
  <rect class="waffle-cell" x="448" y="295" width="52" height="52" fill="#0968F6"/>
  <rect class="waffle-cell" x="504" y="295" width="52" height="52" fill="#0968F6"/>
  <rect class="waffle-cell" x="560" y="295" width="52" height="52" fill="#0968F6"/>
  <rect class="waffle-cell" x="616" y="295" width="52" height="52" fill="#0968F6"/>
  <rect class="waffle-cell" x="672" y="295" width="52" height="52" fill="#0968F6"/>
  <rect class="waffle-cell" x="728" y="295" width="52" height="52" fill="#0968F6"/>
  <rect class="waffle-cell" x="784" y="295" width="52" height="52" fill="#0968F6"/>

  <rect class="waffle-cell" x="280" y="351" width="52" height="52" fill="#0968F6"/>
  <rect class="waffle-cell" x="336" y="351" width="52" height="52" fill="#0968F6"/>
  <rect class="waffle-cell" x="392" y="351" width="52" height="52" fill="#0968F6"/>
  <rect class="waffle-cell" x="448" y="351" width="52" height="52" fill="#0968F6"/>
  <rect class="waffle-cell" x="504" y="351" width="52" height="52" fill="#0968F6"/>
  <rect class="waffle-cell" x="560" y="351" width="52" height="52" fill="#0968F6"/>
  <rect class="waffle-cell" x="616" y="351" width="52" height="52" fill="#0968F6"/>
  <rect class="waffle-cell" x="672" y="351" width="52" height="52" fill="#0968F6"/>
  <rect class="waffle-cell" x="728" y="351" width="52" height="52" fill="#0968F6"/>
  <rect class="waffle-cell" x="784" y="351" width="52" height="52" fill="#0968F6"/>

  <rect class="waffle-cell" x="280" y="407" width="52" height="52" fill="#0968F6"/>
  <rect class="waffle-cell" x="336" y="407" width="52" height="52" fill="#0968F6"/>
  <rect class="waffle-cell" x="392" y="407" width="52" height="52" fill="#0968F6"/>
  <rect class="waffle-cell" x="448" y="407" width="52" height="52" fill="#0968F6"/>
  <rect class="waffle-cell" x="504" y="407" width="52" height="52" fill="#0968F6"/>
  <rect class="waffle-cell" x="560" y="407" width="52" height="52" fill="#0968F6"/>
  <rect class="waffle-cell" x="616" y="407" width="52" height="52" fill="#0968F6"/>
  <rect class="waffle-cell" x="672" y="407" width="52" height="52" fill="#0968F6"/>
  <rect class="waffle-cell" x="728" y="407" width="52" height="52" fill="#0968F6"/>
  <rect class="waffle-cell" x="784" y="407" width="52" height="52" fill="#0968F6"/>

  <rect class="waffle-cell" x="280" y="463" width="52" height="52" fill="#0968F6"/>
  <rect class="waffle-cell" x="336" y="463" width="52" height="52" fill="#0968F6"/>
  <rect class="waffle-cell" x="392" y="463" width="52" height="52" fill="#0968F6"/>
  <rect class="waffle-cell" x="448" y="463" width="52" height="52" fill="#0968F6"/>
  <rect class="waffle-cell" x="504" y="463" width="52" height="52" fill="#0968F6"/>
  <rect class="waffle-cell" x="560" y="463" width="52" height="52" fill="#0968F6"/>
  <rect class="waffle-cell" x="616" y="463" width="52" height="52" fill="#0968F6"/>
  <rect class="waffle-cell" x="672" y="463" width="52" height="52" fill="#0968F6"/>
  <rect class="waffle-cell" x="728" y="463" width="52" height="52" fill="#0968F6"/>
  <rect class="waffle-cell" x="784" y="463" width="52" height="52" fill="#0968F6"/>

  <rect class="waffle-cell" x="280" y="519" width="52" height="52" fill="#0968F6"/>
  <rect class="waffle-cell" x="336" y="519" width="52" height="52" fill="#0968F6"/>
  <rect class="waffle-cell" x="392" y="519" width="52" height="52" fill="#e5e5e5"/>
  <rect class="waffle-cell" x="448" y="519" width="52" height="52" fill="#e5e5e5"/>
  <rect class="waffle-cell" x="504" y="519" width="52" height="52" fill="#e5e5e5"/>
  <rect class="waffle-cell" x="560" y="519" width="52" height="52" fill="#e5e5e5"/>
  <rect class="waffle-cell" x="616" y="519" width="52" height="52" fill="#e5e5e5"/>
  <rect class="waffle-cell" x="672" y="519" width="52" height="52" fill="#e5e5e5"/>
  <rect class="waffle-cell" x="728" y="519" width="52" height="52" fill="#e5e5e5"/>
  <rect class="waffle-cell" x="784" y="519" width="52" height="52" fill="#e5e5e5"/>

  <rect class="waffle-cell" x="280" y="575" width="52" height="52" fill="#e5e5e5"/>
  <rect class="waffle-cell" x="336" y="575" width="52" height="52" fill="#e5e5e5"/>
  <rect class="waffle-cell" x="392" y="575" width="52" height="52" fill="#e5e5e5"/>
  <rect class="waffle-cell" x="448" y="575" width="52" height="52" fill="#e5e5e5"/>
  <rect class="waffle-cell" x="504" y="575" width="52" height="52" fill="#e5e5e5"/>
  <rect class="waffle-cell" x="560" y="575" width="52" height="52" fill="#e5e5e5"/>
  <rect class="waffle-cell" x="616" y="575" width="52" height="52" fill="#e5e5e5"/>
  <rect class="waffle-cell" x="672" y="575" width="52" height="52" fill="#e5e5e5"/>
  <rect class="waffle-cell" x="728" y="575" width="52" height="52" fill="#e5e5e5"/>
  <rect class="waffle-cell" x="784" y="575" width="52" height="52" fill="#e5e5e5"/>

  <rect class="waffle-cell" x="280" y="631" width="52" height="52" fill="#e5e5e5"/>
  <rect class="waffle-cell" x="336" y="631" width="52" height="52" fill="#e5e5e5"/>
  <rect class="waffle-cell" x="392" y="631" width="52" height="52" fill="#e5e5e5"/>
  <rect class="waffle-cell" x="448" y="631" width="52" height="52" fill="#e5e5e5"/>
  <rect class="waffle-cell" x="504" y="631" width="52" height="52" fill="#e5e5e5"/>
  <rect class="waffle-cell" x="560" y="631" width="52" height="52" fill="#e5e5e5"/>
  <rect class="waffle-cell" x="616" y="631" width="52" height="52" fill="#e5e5e5"/>
  <rect class="waffle-cell" x="672" y="631" width="52" height="52" fill="#e5e5e5"/>
  <rect class="waffle-cell" x="728" y="631" width="52" height="52" fill="#e5e5e5"/>
  <rect class="waffle-cell" x="784" y="631" width="52" height="52" fill="#e5e5e5"/>

  <!-- Legend (그리드 오른쪽, 수직 중앙) -->
  <rect x="1000" y="300" width="44" height="44" fill="#0968F6" stroke="#0a0a0a" stroke-width="2.5"/>
  <text x="1064" y="336" font-size="40" font-weight="900">72%</text>
  <text x="1064" y="374" font-size="24" font-weight="700" fill="#616161">채택</text>

  <rect x="1000" y="434" width="44" height="44" fill="#e5e5e5" stroke="#0a0a0a" stroke-width="2.5"/>
  <text x="1064" y="470" font-size="40" font-weight="900">28%</text>
  <text x="1064" y="508" font-size="24" font-weight="700" fill="#616161">미채택</text>
</svg>
</body>
```

Notes: 10x10 그리드로 100% 비율 표현. 좌상단부터 채워나감. 셀 크기 52x52, pitch 56 (gap 4px, 총 556x556). 그리드는 810 캔버스에 수직 중앙(y 127-683). 우측 라벨은 **분리형 범례가 아니라 직접 라벨** — 스와치 + 큰 수치(40px 900) + 짧은 한국어 라벨을 한 덩어리로 밀착시켜 수치가 주인공이 되게 한다(색↔이름 왕복 제거). 예제는 100칸 `<rect>`를 전부 포함한 완성 SVG다 — 그대로 렌더된다. 2 카테고리만 사용 (채운 셀 vs 빈 셀). fill 색상으로 카테고리 구분 (#0968F6 = 활성, #e5e5e5 = 비활성 — 명도차 4.4:1이라 CVD 무관). 퍼센트를 바꾸려면 채운 셀 수만 조정(index = row*10 + col).

---

## 23. Slope (SVG 인라인)

Best for: 전후 정량 변화, 순위 변동, 랭킹 이동, 두 시점 비교

Approach: **SVG inline** — `<line>` + `<circle>` + `<text>`. Y좌표 = rank 기반 배치. JS 불필요.

Max: **5항목**, 2시점 (좌/우 칼럼)

```html
<body>
<svg viewBox="0 0 1440 810" xmlns="http://www.w3.org/2000/svg"
     style="width:1440px;height:810px;background:#f5f5f5">
  <defs>
    <style>
      text { font-family: 'Noto Sans KR', sans-serif; fill: #0a0a0a; }
      .slope-line { stroke-width: 3; fill: none; }
      .slope-dot { stroke: #0a0a0a; stroke-width: 2.5; }
      .header-box { fill: white; stroke: #0a0a0a; stroke-width: 3; }
      .mono { font-family: 'JetBrains Mono', monospace; }
    </style>
    <pattern id="dots" width="16" height="16" patternUnits="userSpaceOnUse">
      <circle cx="8" cy="8" r="1" fill="rgba(10,10,10,0.06)"/>
    </pattern>
  </defs>
  <rect width="1440" height="810" fill="url(#dots)"/>

  <!-- Column headers -->
  <rect class="header-box" x="240" y="90" width="180" height="56" rx="0"/>
  <text x="330" y="127" text-anchor="middle" font-size="28" font-weight="900">2023</text>
  <rect class="header-box" x="1020" y="90" width="180" height="56" rx="0"/>
  <text x="1110" y="127" text-anchor="middle" font-size="28" font-weight="900">2024</text>

  <!-- Y positions: 5 items, y = 210 + (rank-1) * 118 (810 캔버스 세로 중앙) -->
  <!-- Item 1: React — rank 1→3 (y: 210→446) -->
  <line class="slope-line" x1="380" y1="210" x2="1060" y2="446" stroke="#0968F6"/>
  <circle class="slope-dot" cx="380" cy="210" r="10" fill="#0968F6"/>
  <circle class="slope-dot" cx="1060" cy="446" r="10" fill="#0968F6"/>
  <text x="360" y="216" text-anchor="end" font-size="24" font-weight="700">React</text>
  <text x="220" y="216" text-anchor="end" font-size="20" font-weight="700" class="mono" fill="#616161">1</text>
  <text x="1080" y="452" font-size="24" font-weight="700">React</text>
  <text x="1220" y="452" font-size="20" font-weight="700" class="mono" fill="#616161">3</text>

  <!-- Item 2: Svelte — rank 2→1 (y: 328→210) -->
  <line class="slope-line" x1="380" y1="328" x2="1060" y2="210" stroke="#C15100"/>
  <circle class="slope-dot" cx="380" cy="328" r="10" fill="#C15100"/>
  <circle class="slope-dot" cx="1060" cy="210" r="10" fill="#C15100"/>
  <text x="360" y="334" text-anchor="end" font-size="24" font-weight="700">Svelte</text>
  <text x="220" y="334" text-anchor="end" font-size="20" font-weight="700" class="mono" fill="#616161">2</text>
  <text x="1080" y="216" font-size="24" font-weight="700">Svelte</text>
  <text x="1220" y="216" font-size="20" font-weight="700" class="mono" fill="#616161">1</text>

  <!-- Item 3: Vue — rank 3→2 (y: 446→328) -->
  <line class="slope-line" x1="380" y1="446" x2="1060" y2="328" stroke="#288034"/>
  <circle class="slope-dot" cx="380" cy="446" r="10" fill="#288034"/>
  <circle class="slope-dot" cx="1060" cy="328" r="10" fill="#288034"/>
  <text x="360" y="452" text-anchor="end" font-size="24" font-weight="700">Vue</text>
  <text x="220" y="452" text-anchor="end" font-size="20" font-weight="700" class="mono" fill="#616161">3</text>
  <text x="1080" y="334" font-size="24" font-weight="700">Vue</text>
  <text x="1220" y="334" font-size="20" font-weight="700" class="mono" fill="#616161">2</text>

  <!-- Item 4: Angular — rank 4→5 (y: 564→682) -->
  <line class="slope-line" x1="380" y1="564" x2="1060" y2="682" stroke="#DE458E"/>
  <circle class="slope-dot" cx="380" cy="564" r="10" fill="#DE458E"/>
  <circle class="slope-dot" cx="1060" cy="682" r="10" fill="#DE458E"/>
  <text x="360" y="570" text-anchor="end" font-size="24" font-weight="700">Angular</text>
  <text x="220" y="570" text-anchor="end" font-size="20" font-weight="700" class="mono" fill="#616161">4</text>
  <text x="1080" y="688" font-size="24" font-weight="700">Angular</text>
  <text x="1220" y="688" font-size="20" font-weight="700" class="mono" fill="#616161">5</text>

  <!-- Item 5: Solid — rank 5→4 (y: 682→564) -->
  <line class="slope-line" x1="380" y1="682" x2="1060" y2="564" stroke="#583AEE"/>
  <circle class="slope-dot" cx="380" cy="682" r="10" fill="#583AEE"/>
  <circle class="slope-dot" cx="1060" cy="564" r="10" fill="#583AEE"/>
  <text x="360" y="688" text-anchor="end" font-size="24" font-weight="700">Solid</text>
  <text x="220" y="688" text-anchor="end" font-size="20" font-weight="700" class="mono" fill="#616161">5</text>
  <text x="1080" y="570" font-size="24" font-weight="700">Solid</text>
  <text x="1220" y="570" font-size="20" font-weight="700" class="mono" fill="#616161">4</text>
</svg>
</body>
```

Notes: Y좌표 = `210 + (rank-1) * 118` (5항목 기준, 810 캔버스에 세로 중앙 정렬 — 헤더 y=90, 마지막 행 ~688). JS 불필요 — 순수 SVG. **선 색은 선 팔레트에서만**: Blue500 #0968F6 · Green600 #288034 · Red500 #F02D2D · Orange600 #C15100 · Purple500 #583AEE · Teal600 #006F93 · Pink500 #DE458E (연회색 배경 위 실측 3.6~5.9:1). **Yellow 계열(#FFE58A·#EEBB04)과 Green500·Teal500·Orange500은 선 금지**(1.1~2.7:1, 채움면 전용) — 해당 hue 선이 필요하면 600스텝으로 내려라. 좌 칼럼 = 이전 시점, 우 칼럼 = 이후 시점. **축보다 endpoint 직접 라벨**을 우선하고, 5개 이내만 남겨 선 교차를 통제한다. 가능하면 **오른쪽 결과값 기준으로 정렬**해 읽는 부담을 줄인다. **권외 진입·이탈**(한쪽 시점에만 순위가 있는 항목): 순위 리스트 아래에 점선 경계 + "권외" 라벨을 긋고 해당 시점의 순위 자리는 `–`로 표기한다 — 두 시점의 리스트 길이가 달라도 이 문법으로 수용된다.

---

## 26. Dumbbell (SVG 인라인)

Best for: 두 값 사이의 갭/범위 비교, 전후 변화량, 격차 시각화

Approach: **SVG inline** — `<circle>` x2 + `<line>` per row. 공유 x축 선형 매핑. JS 불필요.

Max: **5 rows**, 라벨 max 3단어

```html
<body>
<svg viewBox="0 0 1440 810" xmlns="http://www.w3.org/2000/svg"
     style="width:1440px;height:810px;background:#f5f5f5">
  <defs>
    <style>
      text { font-family: 'Noto Sans KR', sans-serif; fill: #0a0a0a; }
      .db-line { stroke: #e5e5e5; stroke-width: 4; stroke-linecap: round; }
      .db-dot { stroke: #0a0a0a; stroke-width: 2.5; }
      .mono { font-family: 'JetBrains Mono', monospace; }
    </style>
    <pattern id="dots" width="16" height="16" patternUnits="userSpaceOnUse">
      <circle cx="8" cy="8" r="1" fill="rgba(10,10,10,0.06)"/>
    </pattern>
  </defs>
  <rect width="1440" height="810" fill="url(#dots)"/>

  <!-- X axis scale: 0%—100%, mapped to x: 400—1300 -->
  <!-- Scale ticks -->
  <line x1="400" y1="740" x2="1300" y2="740" stroke="#e5e5e5" stroke-width="1.5"/>
  <text class="mono" x="400" y="770" text-anchor="middle" font-size="20" font-weight="700" fill="#616161">0%</text>
  <text class="mono" x="625" y="770" text-anchor="middle" font-size="20" font-weight="700" fill="#616161">25%</text>
  <text class="mono" x="850" y="770" text-anchor="middle" font-size="20" font-weight="700" fill="#616161">50%</text>
  <text class="mono" x="1075" y="770" text-anchor="middle" font-size="20" font-weight="700" fill="#616161">75%</text>
  <text class="mono" x="1300" y="770" text-anchor="middle" font-size="20" font-weight="700" fill="#616161">100%</text>

  <!-- 시점 직접 라벨: 범례 대신 첫 행 endpoint 바로 위, dot과 같은 색 -->
  <text x="1048" y="120" text-anchor="middle" font-size="22" font-weight="900" fill="#0968F6">2023</text>
  <text x="1185" y="120" text-anchor="middle" font-size="22" font-weight="900" fill="#C15100">2024</text>

  <!-- Row 1: React — 2023: 72%, 2024: 85% → x: 1048, 1165 -->
  <text x="360" y="180" text-anchor="end" font-size="24" font-weight="700">React</text>
  <line class="db-line" x1="1048" y1="174" x2="1165" y2="174"/>
  <circle class="db-dot" cx="1048" cy="174" r="12" fill="#0968F6"/>
  <circle class="db-dot" cx="1165" cy="174" r="12" fill="#EC7303"/>
  <text class="mono" x="1030" y="153" text-anchor="end" font-size="20" font-weight="700" fill="#0968F6">72</text>
  <text class="mono" x="1185" y="153" font-size="20" font-weight="700" fill="#C15100">85</text>
  <text class="mono" x="1208" y="180" font-size="20" font-weight="700" fill="#1B561A">+13</text>

  <!-- Row 2: Vue — 2023: 45%, 2024: 62% → x: 805, 958 -->
  <text x="360" y="310" text-anchor="end" font-size="24" font-weight="700">Vue</text>
  <line class="db-line" x1="805" y1="304" x2="958" y2="304"/>
  <circle class="db-dot" cx="805" cy="304" r="12" fill="#0968F6"/>
  <circle class="db-dot" cx="958" cy="304" r="12" fill="#EC7303"/>
  <text class="mono" x="787" y="283" text-anchor="end" font-size="20" font-weight="700" fill="#0968F6">45</text>
  <text class="mono" x="978" y="283" font-size="20" font-weight="700" fill="#C15100">62</text>
  <text class="mono" x="1000" y="310" font-size="20" font-weight="700" fill="#1B561A">+17</text>

  <!-- Row 3: Svelte — 2023: 28%, 2024: 55% → x: 652, 895 -->
  <text x="360" y="440" text-anchor="end" font-size="24" font-weight="700">Svelte</text>
  <line class="db-line" x1="652" y1="434" x2="895" y2="434"/>
  <circle class="db-dot" cx="652" cy="434" r="12" fill="#0968F6"/>
  <circle class="db-dot" cx="895" cy="434" r="12" fill="#EC7303"/>
  <text class="mono" x="634" y="413" text-anchor="end" font-size="20" font-weight="700" fill="#0968F6">28</text>
  <text class="mono" x="915" y="413" font-size="20" font-weight="700" fill="#C15100">55</text>
  <text class="mono" x="940" y="440" font-size="20" font-weight="700" fill="#1B561A">+27</text>

  <!-- Row 4: Angular — 2023: 60%, 2024: 42% → x: 940, 778 -->
  <text x="360" y="570" text-anchor="end" font-size="24" font-weight="700">Angular</text>
  <line class="db-line" x1="778" y1="564" x2="940" y2="564"/>
  <circle class="db-dot" cx="940" cy="564" r="12" fill="#0968F6"/>
  <circle class="db-dot" cx="778" cy="564" r="12" fill="#EC7303"/>
  <text class="mono" x="960" y="543" font-size="20" font-weight="700" fill="#0968F6">60</text>
  <text class="mono" x="758" y="543" text-anchor="end" font-size="20" font-weight="700" fill="#C15100">42</text>
  <text class="mono" x="980" y="570" font-size="20" font-weight="700" fill="#D50B0B">-18</text>

  <!-- Row 5: Solid — 2023: 10%, 2024: 35% → x: 490, 715 -->
  <text x="360" y="670" text-anchor="end" font-size="24" font-weight="700">Solid</text>
  <line class="db-line" x1="490" y1="664" x2="715" y2="664"/>
  <circle class="db-dot" cx="490" cy="664" r="12" fill="#0968F6"/>
  <circle class="db-dot" cx="715" cy="664" r="12" fill="#EC7303"/>
  <text class="mono" x="472" y="643" text-anchor="end" font-size="20" font-weight="700" fill="#0968F6">10</text>
  <text class="mono" x="735" y="643" font-size="20" font-weight="700" fill="#C15100">35</text>
  <text class="mono" x="758" y="670" font-size="20" font-weight="700" fill="#1B561A">+25</text>
</svg>
</body>
```

Notes: x축 범위 400~1300px, 값 0~100%를 선형 매핑 (`x = 400 + value/100 * 900`). 각 행에 연결 선(muted) + 양끝 dot(colored)으로 갭 시각화. **범례를 두지 말고 직접 라벨링** — 시점 라벨(2023/2024)은 첫 행 endpoint 바로 위에 dot과 같은 색으로 1회만 붙이면 이후 행은 색으로 이어 읽힌다. endpoint 값·delta도 직접 라벨. dot 면은 Blue500/Orange500(CVD-safe 축), **값 텍스트는 진한 스텝**(Blue500 4.5·Orange600 4.3 — Orange500 텍스트는 2.7:1 미달). 비교용 dumbbell은 보통 **최신값이나 변화량 기준 정렬**이 가장 자연스럽다.

---

## 28. Bullet (SVG 인라인)

Best for: 실적 vs 목표, KPI 달성률, 맥락 포함 정량 지표

Approach: **SVG inline** — 중첩 `<rect>` (배경 범위 3단계) + 전경 actual 바 + 타겟 `<line>`.

Max: **3~4 charts** 수직 배치

```html
<body>
<svg viewBox="0 0 1440 810" xmlns="http://www.w3.org/2000/svg"
     style="width:1440px;height:810px;background:#f5f5f5">
  <defs>
    <style>
      text { font-family: 'Noto Sans KR', sans-serif; fill: #0a0a0a; }
      .mono { font-family: 'JetBrains Mono', monospace; }
      .range { stroke: none; }
      .actual { stroke: #0a0a0a; stroke-width: 3; }
      .target { stroke: #0a0a0a; stroke-width: 4; }
    </style>
    <pattern id="dots" width="16" height="16" patternUnits="userSpaceOnUse">
      <circle cx="8" cy="8" r="1" fill="rgba(10,10,10,0.06)"/>
    </pattern>
  </defs>
  <rect width="1440" height="810" fill="url(#dots)"/>

  <!-- Bullet chart layout: x range 350-1300, bar height 60, spacing 190 -->
  <!-- Scale: 0-100 mapped to x: 350-1300 (950px range) -->

  <!-- Chart 1: 매출 — ranges: poor 0-40, ok 40-75, good 75-100 | actual: 82 | target: 90 -->
  <text x="320" y="180" text-anchor="end" font-size="28" font-weight="900">매출</text>
  <!-- Range backgrounds (back-to-front: widest=lightest first) -->
  <rect class="range" x="350" y="150" width="950" height="60" fill="#e5e5e5"/>
  <rect class="range" x="350" y="150" width="713" height="60" fill="#d4d4d4"/>
  <rect class="range" x="350" y="150" width="380" height="60" fill="#8F8F8F"/>
  <!-- Actual bar (범위 밴드 60px보다 얇은 44px, 밴드 안 수직 중앙 = y+8) -->
  <rect class="actual" x="350" y="158" width="779" height="44" fill="#0968F6"/>
  <!-- Target marker -->
  <line class="target" x1="1205" y1="145" x2="1205" y2="215"/>
  <text class="mono" x="1205" y="238" text-anchor="middle" font-size="20" font-weight="700" fill="#616161">90</text>
  <text class="mono" x="1145" y="187" text-anchor="start" font-size="20" font-weight="700" fill="#0968F6">82</text>

  <!-- Chart 2: 성장률 — ranges: poor 0-30, ok 30-60, good 60-100 | actual: 68 | target: 50 -->
  <text x="320" y="370" text-anchor="end" font-size="28" font-weight="900">성장률</text>
  <rect class="range" x="350" y="340" width="950" height="60" fill="#e5e5e5"/>
  <rect class="range" x="350" y="340" width="570" height="60" fill="#d4d4d4"/>
  <rect class="range" x="350" y="340" width="285" height="60" fill="#8F8F8F"/>
  <rect class="actual" x="350" y="348" width="646" height="44" fill="#0968F6"/>
  <line class="target" x1="825" y1="335" x2="825" y2="405"/>
  <text class="mono" x="825" y="428" text-anchor="middle" font-size="20" font-weight="700" fill="#616161">50</text>
  <text class="mono" x="1012" y="377" font-size="20" font-weight="700" fill="#0968F6">68</text>

  <!-- Chart 3: NPS — ranges: poor 0-30, ok 30-70, good 70-100 | actual: 55 | target: 70 -->
  <text x="320" y="560" text-anchor="end" font-size="28" font-weight="900">NPS</text>
  <rect class="range" x="350" y="530" width="950" height="60" fill="#e5e5e5"/>
  <rect class="range" x="350" y="530" width="665" height="60" fill="#d4d4d4"/>
  <rect class="range" x="350" y="530" width="285" height="60" fill="#8F8F8F"/>
  <rect class="actual" x="350" y="538" width="523" height="44" fill="#0968F6"/>
  <line class="target" x1="1015" y1="525" x2="1015" y2="595"/>
  <text class="mono" x="1015" y="618" text-anchor="middle" font-size="20" font-weight="700" fill="#616161">70</text>
  <text class="mono" x="889" y="567" font-size="20" font-weight="700" fill="#0968F6">55</text>

  <!-- Range labels (single row) -->
  <text x="350" y="720" font-size="20" font-weight="700" fill="#616161">정성 범위</text>
  <rect x="470" y="700" width="24" height="20" fill="#8F8F8F"/>
  <text x="506" y="717" font-size="20" font-weight="700" fill="#616161">부진</text>
  <rect x="576" y="700" width="24" height="20" fill="#d4d4d4"/>
  <text x="612" y="717" font-size="20" font-weight="700" fill="#616161">보통</text>
  <rect x="682" y="700" width="24" height="20" fill="#e5e5e5"/>
  <text x="718" y="717" font-size="20" font-weight="700" fill="#616161">양호</text>
  <line x1="816" y1="700" x2="816" y2="722" stroke="#0a0a0a" stroke-width="4"/>
  <text x="834" y="717" font-size="20" font-weight="700" fill="#616161">목표</text>
</svg>
</body>
```

Notes: Back-to-front 레이어링으로 3단계 범위 표현 (가장 넓은 rect = lightest, 점점 좁고 진함). Actual 바는 범위 밴드(60px)보다 얇은 44px로, 밴드 안에 수직 중앙(band_y + (60-44)/2 = band_y + 8) 정렬해 위·아래 여백을 각 8px로 맞춘다. Target marker는 `<line>` (stroke-width: 4). x축 스케일: `x = 350 + (value/100) * 950`. **정성 구간은 muted, actual은 일관된 단일 색상, 값은 바 끝에 직접 표기**하는 편이 가장 읽기 쉽다.

---

## 30. Waterfall (SVG 인라인)

Best for: 증감 분해, 누적 변화, 수익 분석, 요인별 기여도

Approach: **SVG inline** — floating `<rect>` (증가/감소) + grounded `<rect>` (시작/합계) + connector `<line>`. JS 불필요.

Max: **6~8 bars**, 라벨 1~2단어

```html
<body>
<svg viewBox="0 0 1440 810" xmlns="http://www.w3.org/2000/svg"
     style="width:1440px;height:810px;background:#f5f5f5">
  <defs>
    <style>
      text { font-family: 'Noto Sans KR', sans-serif; fill: #0a0a0a; }
      .bar { stroke: #0a0a0a; stroke-width: 3; }
      .bar-sh { fill: #0a0a0a; opacity: 0.08; stroke: none; }
      .connector { stroke: #616161; stroke-width: 5; stroke-dasharray: 12 8; }
      .mono { font-family: 'JetBrains Mono', monospace; }
      .pos { fill: #3CC14E; }
      .neg { fill: #F02D2D; }
      .total { fill: #0968F6; }
    </style>
    <pattern id="dots" width="16" height="16" patternUnits="userSpaceOnUse">
      <circle cx="8" cy="8" r="1" fill="rgba(10,10,10,0.06)"/>
    </pattern>
  </defs>
  <rect width="1440" height="810" fill="url(#dots)"/>

  <!-- Scale: value 0-180 → y: 650→120 (530px). y(v) = 650 - (v/180)*530 -->
  <!-- Bar width: 120px, spacing: 180px, starting x: 200 -->
  <!-- Data: Start=100, +Revenue=40, +Services=25, -COGS=30, -OpEx=20, Total=115 -->

  <!-- Bar 1: 시작 (grounded: 0→100) y(100)=356, h=294 -->
  <rect class="bar-sh" x="204" y="360" width="120" height="294"/>
  <rect class="bar total" x="200" y="356" width="120" height="294"/>
  <text class="mono" x="260" y="340" text-anchor="middle" font-size="22" font-weight="700">100</text>
  <text x="260" y="700" text-anchor="middle" font-size="22" font-weight="900">시작</text>

  <!-- Connector: y=356 from x=320 to x=380 -->
  <line class="connector" x1="320" y1="356" x2="380" y2="356"/>

  <!-- Bar 2: +매출 (floating: 100→140) y(140)=238, h=118 -->
  <rect class="bar-sh" x="384" y="242" width="120" height="118"/>
  <rect class="bar pos" x="380" y="238" width="120" height="118"/>
  <text class="mono" x="440" y="222" text-anchor="middle" font-size="22" font-weight="700" fill="#1B561A">+40</text>
  <text x="440" y="700" text-anchor="middle" font-size="22" font-weight="900">매출</text>

  <!-- Connector: y=238 from x=500 to x=560 -->
  <line class="connector" x1="500" y1="238" x2="560" y2="238"/>

  <!-- Bar 3: +서비스 (floating: 140→165) y(165)=164, h=74 -->
  <rect class="bar-sh" x="564" y="168" width="120" height="74"/>
  <rect class="bar pos" x="560" y="164" width="120" height="74"/>
  <text class="mono" x="620" y="148" text-anchor="middle" font-size="22" font-weight="700" fill="#1B561A">+25</text>
  <text x="620" y="700" text-anchor="middle" font-size="22" font-weight="900">서비스</text>

  <!-- Connector: y=164 from x=680 to x=740 -->
  <line class="connector" x1="680" y1="164" x2="740" y2="164"/>

  <!-- Bar 4: -원가 (floating: 165→135) top=y(165)=164, bottom=y(135)=252, h=88 -->
  <rect class="bar-sh" x="744" y="168" width="120" height="88"/>
  <rect class="bar neg" x="740" y="164" width="120" height="88"/>
  <text class="mono" x="800" y="272" text-anchor="middle" font-size="22" font-weight="700" fill="#D50B0B">-30</text>
  <text x="800" y="700" text-anchor="middle" font-size="22" font-weight="900">원가</text>

  <!-- Connector: y=252 from x=860 to x=920 -->
  <line class="connector" x1="860" y1="252" x2="920" y2="252"/>

  <!-- Bar 5: -운영비 (floating: 135→115) top=y(135)=252, bottom=y(115)=311, h=59 -->
  <rect class="bar-sh" x="924" y="256" width="120" height="59"/>
  <rect class="bar neg" x="920" y="252" width="120" height="59"/>
  <text class="mono" x="980" y="331" text-anchor="middle" font-size="22" font-weight="700" fill="#D50B0B">-20</text>
  <text x="980" y="700" text-anchor="middle" font-size="22" font-weight="900">운영비</text>

  <!-- Connector: y=311 from x=1040 to x=1100 -->
  <line class="connector" x1="1040" y1="311" x2="1100" y2="311"/>

  <!-- Bar 6: 합계 (grounded: 0→115) y(115)=311, h=339 -->
  <rect class="bar-sh" x="1104" y="315" width="120" height="339"/>
  <rect class="bar total" x="1100" y="311" width="120" height="339"/>
  <text class="mono" x="1160" y="295" text-anchor="middle" font-size="22" font-weight="700">115</text>
  <text x="1160" y="700" text-anchor="middle" font-size="22" font-weight="900">합계</text>

  <!-- Baseline -->
  <line x1="170" y1="650" x2="1250" y2="650" stroke="#e5e5e5" stroke-width="1.5"/>

  <!-- Legend -->
  <rect x="200" y="760" width="20" height="20" fill="#3CC14E" stroke="#0a0a0a" stroke-width="2"/>
  <text x="230" y="777" font-size="20" font-weight="700" fill="#616161">증가</text>
  <rect x="310" y="760" width="20" height="20" fill="#F02D2D" stroke="#0a0a0a" stroke-width="2"/>
  <text x="340" y="777" font-size="20" font-weight="700" fill="#616161">감소</text>
  <rect x="420" y="760" width="20" height="20" fill="#0968F6" stroke="#0a0a0a" stroke-width="2"/>
  <text x="450" y="777" font-size="20" font-weight="700" fill="#616161">합계</text>
</svg>
</body>
```

Notes: Floating rect로 증감 표현 — 증가 바는 이전 누적값 위에 쌓이고, 감소 바는 이전 누적값에서 아래로 내려감. Grounded bar (시작/합계)는 baseline(y=650)에서 시작. Connector (dashed line, **5px #616161**)가 이전 바의 끝점과 다음 바의 시작점을 연결 — 1.5px 연회색은 25% 축소에서 소멸해 바들이 공중에 떠 보인다. 값 라벨: 증가는 바 위 (#1B561A Green700), 감소는 바 아래 (#D50B0B Red600). 증가/감소 면은 **Green500/Red500 채움면**(검정 3px 보더 + 외부 라벨)으로, 명도차(2.1:1)와 +/− 부호·상하 방향이 함께 전달되어 CVD에서도 구분이 살아남는다 — 색에만 기대지 마라. `y(v) = 650 - (v/180) * 530` 스케일. JS 불필요.

---
