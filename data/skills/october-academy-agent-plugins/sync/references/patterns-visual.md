# Figure Patterns — Visual / Generative

Visual & generative patterns (5): Isometric, IconDiagram, Network, Graph, Typographic Statement.

All use `assets/figure.css`. SVG 인라인, Canvas, D3 등 기술별 접근 방식이 다름.

## TOC

- 17. Isometric
- 18. IconDiagram
- 19. Network
- 20. Graph
- 22. Typographic Statement

---

## 17. Isometric (SVG 인라인)

Best for: 3D 블록 구조, 레이어 시각화, 아이소메트릭 와이어프레임, 개념의 공간적 관계

Approach: **SVG inline** — 정밀한 도형 배치. 외부 의존성 없음. `<polygon>` 조합으로 아이소메트릭 큐브.

Max: **4 블록**. 블록당 라벨 1단어.

```html
<body>
<svg viewBox="0 0 1440 810" xmlns="http://www.w3.org/2000/svg"
     style="width:1440px;height:810px;background:#f5f5f5">
  <defs>
    <style>
      text { font-family: 'Noto Sans KR', sans-serif; fill: #0a0a0a; }
      .iso { stroke: #0a0a0a; stroke-width: 2.5; stroke-linejoin: round; }
    </style>
    <!-- Dot grid background -->
    <pattern id="dots" width="16" height="16" patternUnits="userSpaceOnUse">
      <circle cx="8" cy="8" r="1" fill="rgba(10,10,10,0.06)"/>
    </pattern>
  </defs>
  <rect width="1440" height="810" fill="url(#dots)"/>

  <!-- Isometric cube: top=light, left=mid, right=dark of same hue
       Position with translate(cx, cy). cy = bottom center of cube. -->

  <!-- Layer 1: Data platform (bottom, largest). Label on front-left face. -->
  <g transform="translate(360, 570)">
    <polygon class="iso" fill="#84B4FB" points="0,-70 360,-170 720,-70 360,30"/>
    <polygon class="iso" fill="#70A9FF" points="0,-70 0,70 360,170 360,30"/>
    <polygon class="iso" fill="#0968F6" points="360,30 360,170 720,70 720,-70"/>
    <text x="180" y="50" text-anchor="middle" dominant-baseline="central" font-size="34" font-weight="900">데이터</text>
  </g>

  <!-- Layer 2: Backend -->
  <g transform="translate(470, 430)">
    <polygon class="iso" fill="#A6F0A5" points="0,-60 250,-125 500,-60 250,5"/>
    <polygon class="iso" fill="#89F598" points="0,-60 0,50 250,115 250,5"/>
    <polygon class="iso" fill="#3CC14E" points="250,5 250,115 500,50 500,-60"/>
    <text x="125" y="28" text-anchor="middle" dominant-baseline="central" font-size="30" font-weight="900">백엔드</text>
  </g>

  <!-- Layer 3: API -->
  <g transform="translate(550, 300)">
    <polygon class="iso" fill="#FFE58A" points="0,-48 170,-100 340,-48 170,4"/>
    <polygon class="iso" fill="#FFBD14" points="0,-48 0,35 170,87 170,4"/>
    <polygon class="iso" fill="#EEBB04" points="170,4 170,87 340,35 340,-48"/>
    <text x="85" y="20" text-anchor="middle" dominant-baseline="central" font-size="28" font-weight="900">API</text>
  </g>

  <!-- Layer 4: UI -->
  <g transform="translate(600, 195)">
    <polygon class="iso" fill="#F79CC8" points="0,-42 120,-82 240,-42 120,-2"/>
    <polygon class="iso" fill="#F155A0" points="0,-42 0,24 120,64 120,-2"/>
    <polygon class="iso" fill="#DE458E" points="120,-2 120,64 240,24 240,-42"/>
    <text x="60" y="11" text-anchor="middle" dominant-baseline="central" font-size="24" font-weight="900">UI</text>
  </g>
</svg>
</body>
```

Notes: 각 면에 같은 색조의 3단계 명도를 적용(top=light, left=mid, right=dark). `translate(cx, cy)`로 블록 위치 조정 — 각 블록의 top face 중심을 **x=720에 맞춰 수평 중앙 정렬**한다. **최하단 블록 폭을 크게 잡고 4단 적층**으로 만들면 아이소메트릭 패턴의 under-fill이 크게 줄어든다. 라벨은 top face에 두면 위 블록에 가려 잘리므로 각 블록의 **front-left face 중앙**(`text-anchor="middle"` + `dominant-baseline="central"`)에 배치한다.

---

## 18. IconDiagram (SVG 인라인)

Best for: 시스템 다이어그램, 기술 구성도, 아이콘 기반 노드와 커넥터, 요청/응답 흐름

Approach: **SVG inline** — 노드(아이콘 + 라벨 박스) + 커넥터(화살표 `<marker>`) 조합.

Max: **4 노드**, **4 커넥터**. 아이콘은 기본 SVG 도형으로 구성 (circle, rect, path).

```html
<body>
<svg viewBox="0 0 1440 810" xmlns="http://www.w3.org/2000/svg"
     style="width:1440px;height:810px;background:#f5f5f5">
  <defs>
    <style>
      text { font-family: 'Noto Sans KR', sans-serif; fill: #0a0a0a; }
      .box { fill: white; stroke: #0a0a0a; stroke-width: 3; }
      .box-sh { fill: #0a0a0a; }
      .conn { stroke: #0a0a0a; stroke-width: 6; fill: none; }
    </style>
    <!-- markerUnits="userSpaceOnUse": 화살촉을 stroke 굵기와 무관하게 24px로 고정 -->
    <marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse"
            markerWidth="24" markerHeight="24" orient="auto-start-reverse">
      <path d="M0 0L10 5L0 10z" fill="#0a0a0a"/>
    </marker>
    <pattern id="dots" width="16" height="16" patternUnits="userSpaceOnUse">
      <circle cx="8" cy="8" r="1" fill="rgba(10,10,10,0.06)"/>
    </pattern>
  </defs>
  <rect width="1440" height="810" fill="url(#dots)"/>

  <!-- Node: User -->
  <g transform="translate(160, 294)">
    <rect class="box-sh" x="4" y="4" width="210" height="160" rx="12"/>
    <rect class="box" width="210" height="160" rx="12"/>
    <!-- Person icon: head + shoulders -->
    <circle cx="105" cy="45" r="20" fill="none" stroke="#0968F6" stroke-width="3"/>
    <path d="M70 95 Q105 72 140 95" fill="none" stroke="#0968F6" stroke-width="3"/>
    <text x="105" y="138" text-anchor="middle" font-size="28" font-weight="900">사용자</text>
  </g>

  <!-- Node: Gateway -->
  <g transform="translate(520, 174)">
    <rect class="box-sh" x="4" y="4" width="220" height="170" rx="12"/>
    <rect class="box" width="220" height="170" rx="12"/>
    <!-- Gear icon: circle + center dot — 아이콘 선도 선 팔레트(lime 금지 → dark green) -->
    <circle cx="110" cy="52" r="26" fill="none" stroke="#288034" stroke-width="3"/>
    <circle cx="110" cy="52" r="8" fill="#288034"/>
    <text x="110" y="144" text-anchor="middle" font-size="28" font-weight="900">Gateway</text>
  </g>

  <!-- Node: Queue -->
  <g transform="translate(520, 474)">
    <rect class="box-sh" x="4" y="4" width="220" height="160" rx="12"/>
    <rect class="box" width="220" height="160" rx="12"/>
    <rect x="70" y="34" width="80" height="52" rx="8" fill="none" stroke="#583AEE" stroke-width="3"/>
    <path d="M70 60 h80" fill="none" stroke="#583AEE" stroke-width="3"/>
    <text x="110" y="138" text-anchor="middle" font-size="28" font-weight="900">Queue</text>
  </g>

  <!-- Node: DB -->
  <g transform="translate(1070, 329)">
    <rect class="box-sh" x="4" y="4" width="210" height="170" rx="12"/>
    <rect class="box" width="210" height="170" rx="12"/>
    <!-- Cylinder icon: ellipse + body -->
    <ellipse cx="105" cy="42" rx="34" ry="14" fill="none" stroke="#C15100" stroke-width="3"/>
    <path d="M71 42 v40 a34 14 0 0 0 68 0 v-40" fill="none" stroke="#C15100" stroke-width="3"/>
    <text x="105" y="144" text-anchor="middle" font-size="28" font-weight="900">DB</text>
  </g>

  <!-- Connectors with arrow markers -->
  <line class="conn" x1="370" y1="374" x2="520" y2="259" marker-end="url(#arr)"/>
  <text x="445" y="289" text-anchor="middle" font-size="20" font-weight="700" fill="#616161">요청</text>

  <line class="conn" x1="740" y1="259" x2="1070" y2="394" marker-end="url(#arr)"/>
  <text x="915" y="299" text-anchor="middle" font-size="20" font-weight="700" fill="#616161">쿼리</text>

  <line class="conn" x1="740" y1="554" x2="1070" y2="434" marker-end="url(#arr)"/>
  <text x="915" y="514" text-anchor="middle" font-size="20" font-weight="700" fill="#616161">이벤트</text>

  <line class="conn" x1="630" y1="344" x2="630" y2="474" marker-end="url(#arr)"/>
  <text x="660" y="416" font-size="20" font-weight="700" fill="#616161">비동기 처리</text>
</svg>
</body>
```

Notes: 아이콘은 기본 SVG 도형(circle, ellipse, path, rect)으로 구성. 외부 아이콘 라이브러리 불필요. `<marker>` 로 화살표 정의하고 `marker-end="url(#arr)"`으로 적용. 커넥터는 **stroke-width 6 + 화살촉 24px** — 2~3px 선은 25% 축소에서 소멸한다. `markerUnits="userSpaceOnUse"`를 줘야 화살촉 크기가 stroke 굵기에 비례해 커지지 않고 고정된다. **4노드 + 4커넥터**(수평 3 + 수직 1) 정도가 가장 완성도가 높고, 수평/수직 연결을 섞으면 캔버스 활용도가 훨씬 좋아진다. 노드 bounding box의 중심을 캔버스 중앙(720, 405)에 맞춰 배치해야 특정 모서리로 쏠리지 않는다.

---

## 19. Network (Canvas/JS)

Best for: 노드 네트워크, 결정론적 그리드 ↔ 확률적 스캐터 대비, 추상적 관계 시각화, 하이브리드 네트워크

Approach: **Canvas** — JS로 노드/엣지를 직접 그림. retina 2x. `document.fonts.ready`로 폰트 로드 후 렌더링.

참고: [Zed Agentic Engineering](https://zed.dev/agentic-engineering) FIG 1/2/3 스타일.

Config: `nodes` 배열과 `edges` 배열만 수정하면 내용 변경 가능.

```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=1440">
  <link rel="stylesheet" href="file://{SKILL_DIR}/assets/figure.css">
</head>
<body style="margin:0;overflow:hidden;background:var(--card)">
<canvas id="c" width="2880" height="1620" style="width:1440px;height:810px;display:block"></canvas>
<script>
document.fonts.ready.then(() => {
const C = document.getElementById('c'), ctx = C.getContext('2d');
const S = 2; // retina scale

// === PALETTE (matches figure.css tokens) ===
const P = {
  dark:'#0a0a0a', muted:'#616161', bg:'#f5f5f5', card:'#e5e5e5',
  blue:'#0968F6', lime:'#3CC14E', orange:'#EC7303',
  purple:'#583AEE', pink:'#DE458E', yellow:'#FFE58A'
};

// === CONFIG: Modify nodes/edges for your content ===

// Section A: Deterministic grid (left half)
const gridNodes = [];
for (let r = 0; r < 3; r++)
  for (let c = 0; c < 7; c++)
    gridNodes.push({
      x: 150 + c * 76, y: 310 + r * 88, r: 26,
      color: P.card, label: (c + r) % 2 ? '1' : '0', opacity: 0.85
    });

// Section B: Stochastic scatter (right half)
const scatterNodes = [
  { x:840,  y:180, r:42, color:P.blue,   label:'0.8', opacity:0.85 },
  { x:965,  y:250, r:22, color:P.lime,   label:'0.3', opacity:0.5 },
  { x:1090, y:200, r:28, color:P.orange, label:'0.9', opacity:0.7 },
  { x:1195, y:160, r:20, color:P.purple, label:'0.4', opacity:0.45 },
  { x:1290, y:235, r:32, color:P.pink,   label:'0.7', opacity:0.75 },
  { x:885,  y:340, r:18, color:P.yellow, label:'0.1', opacity:0.4 },
  { x:1015, y:395, r:50, color:P.blue,   label:'1.0', opacity:0.75 },
  { x:1150, y:345, r:26, color:P.lime,   label:'0.5', opacity:0.55 },
  { x:1265, y:390, r:35, color:P.orange, label:'0.2', opacity:0.5 },
  { x:885,  y:485, r:24, color:P.purple, label:'0.6', opacity:0.6 },
  { x:1025, y:520, r:30, color:P.pink,   label:'0.2', opacity:0.45 },
  { x:1180, y:485, r:38, color:P.yellow, label:'0.8', opacity:0.7 },
  { x:1290, y:520, r:20, color:P.blue,   label:'0.3', opacity:0.4 },
  { x:950,  y:590, r:34, color:P.lime,   label:'0.9', opacity:0.8 },
  { x:1120, y:600, r:22, color:P.orange, label:'0.3', opacity:0.5 },
];

const all = [...gridNodes, ...scatterNodes];

// Auto-generate edges between nearby scatter nodes
const edges = [];
const sOff = gridNodes.length;
for (let i = sOff; i < all.length; i++)
  for (let j = i + 1; j < all.length; j++) {
    const d = Math.hypot(all[i].x - all[j].x, all[i].y - all[j].y);
    if (d < 220) edges.push([i, j, 0.25 + Math.random() * 0.1]);
  }

// === RENDER ===
ctx.fillStyle = P.bg;
ctx.fillRect(0, 0, 2880, 1620);

// Dot grid background
ctx.fillStyle = 'rgba(10,10,10,0.05)';
for (let x = 0; x < 2880; x += 32)
  for (let y = 0; y < 1620; y += 32) {
    ctx.beginPath(); ctx.arc(x, y, 1.5, 0, Math.PI * 2); ctx.fill();
  }

// Divider line (subtle)
ctx.strokeStyle = 'rgba(10,10,10,0.08)';
ctx.lineWidth = 1.5 * S;
ctx.setLineDash([8 * S, 6 * S]);
ctx.beginPath(); ctx.moveTo(720 * S, 130 * S); ctx.lineTo(720 * S, 650 * S); ctx.stroke();
ctx.setLineDash([]);

// Edges
edges.forEach(([i, j, a]) => {
  ctx.beginPath();
  ctx.moveTo(all[i].x * S, all[i].y * S);
  ctx.lineTo(all[j].x * S, all[j].y * S);
  ctx.strokeStyle = `rgba(10,10,10,${a})`;
  ctx.lineWidth = 2 * S;
  ctx.stroke();
});

// Nodes
all.forEach(n => {
  const x = n.x * S, y = n.y * S, r = n.r * S;
  ctx.globalAlpha = n.opacity;
  ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI * 2);
  ctx.fillStyle = n.color; ctx.fill();
  ctx.globalAlpha = 1;
  ctx.strokeStyle = P.dark; ctx.lineWidth = 3 * S; ctx.stroke();
  // Label
  ctx.fillStyle = P.dark;
  ctx.font = `700 ${Math.max(14, n.r * 0.55) * S}px 'Noto Sans KR'`;
  ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
  ctx.fillText(n.label, x, y + S);
});

// Section labels (monospace, top)
ctx.font = `500 ${20 * S}px 'JetBrains Mono'`;
ctx.fillStyle = P.muted; ctx.textAlign = 'left';
ctx.fillText('[ FIG 1 ] \u2014 DETERMINISTIC', 100 * S, 100 * S);
ctx.fillText('[ FIG 2 ] \u2014 STOCHASTIC', 800 * S, 100 * S);

// Captions (bottom, keep a 100px safety gutter to avoid clipping)
ctx.font = `700 ${20 * S}px 'Noto Sans KR'`;
ctx.textAlign = 'center';
ctx.fillText('\uADDC\uCE59 \uAE30\uBC18, \uC608\uCE21 \uAC00\uB2A5\uD55C \uACB0\uACFC', 390 * S, 690 * S);
ctx.fillText('\uC720\uB3D9\uC801, \uD655\uB960\uC801 \uD0D0\uC0C9', 1060 * S, 690 * S);
});
</script>
</body>
```

Notes: `document.fonts.ready.then()`으로 감싸야 Canvas에서 Google Fonts가 정상 렌더링됨. `S = 2`로 retina 해상도 출력 (canvas 2880×1620 → CSS 1440×810). 노드 `opacity`로 확률적 느낌 표현. 그리드 노드는 균일 크기/색상, 스캐터 노드는 다양한 크기/색상/투명도. edges는 가까운 노드 자동 연결 — alpha를 **0.25~0.35**로 둬 25% 축소에서도 엣지가 보이게 한다(더 연하면 노드만 떠 보인다). 하단 캡션은 **100px safety gutter** 안에 두고 inline font를 **20px 이상** 유지한다. `\u` 이스케이프는 "규칙 기반, 예측 가능한 결과" / "유동적, 확률적 탐색" — 한글 텍스트를 Canvas에 직접 쓸 때 사용.

---

## 20. Graph (D3)

Best for: 포스-다이렉티드 그래프, 노드-링크 다이어그램, 개념 간 자동 배치 관계도

Approach: **D3 v7 CDN** — 물리 시뮬레이션으로 노드 자동 배치. `sim.tick()` 동기 실행 후 캡처.

Config: `nodes`와 `links` 배열만 수정하면 내용 변경 가능.

```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=1440">
  <link rel="stylesheet" href="file://{SKILL_DIR}/assets/figure.css">
  <script src="https://d3js.org/d3.v7.min.js"></script>
  <style>
    body { width:1440px;height:810px;margin:0;overflow:hidden;background:#f5f5f5; }
    .link { stroke:#404040; stroke-width:3; }
    .node { stroke:#0a0a0a; stroke-width:3; }
    .label { font-family:'Noto Sans KR',sans-serif; font-weight:700; font-size:20px;
             fill:#0a0a0a; text-anchor:middle; dominant-baseline:central; }
  </style>
</head>
<body>
<svg width="1440" height="810">
  <defs>
    <pattern id="dots" width="16" height="16" patternUnits="userSpaceOnUse">
      <circle cx="8" cy="8" r="1" fill="rgba(10,10,10,0.06)"/>
    </pattern>
  </defs>
  <rect width="1440" height="810" fill="url(#dots)"/>
</svg>
<script>
// === CONFIG: Modify for your content ===
const nodes = [
  { id: '문제 정의', group: 1, r: 40 },
  { id: '인터뷰',   group: 1, r: 35 },
  { id: 'SPEC',     group: 2, r: 30 },
  { id: '개발',     group: 2, r: 35 },
  { id: '배포',     group: 3, r: 30 },
  { id: '검증',     group: 3, r: 32 },
  { id: '피봇',     group: 1, r: 25 },
  { id: '로그',     group: 3, r: 24 },
  { id: '지표',     group: 2, r: 24 },
];
const links = [
  { source: '문제 정의', target: '인터뷰' },
  { source: '인터뷰',   target: 'SPEC' },
  { source: 'SPEC',     target: '개발' },
  { source: '개발',     target: '배포' },
  { source: '배포',     target: '검증' },
  { source: '검증',     target: '피봇' },
  { source: '피봇',     target: '문제 정의' },
  { source: '인터뷰',   target: '검증' },
  { source: '배포',     target: '로그' },
  { source: '로그',     target: '지표' },
  { source: '지표',     target: '검증' },
  { source: '개발',     target: '지표' },
];
const groupColor = { 1: '#0968F6', 2: '#3CC14E', 3: '#EC7303' };

const svg = d3.select('svg');
const W = 1440, H = 810;

// Deterministic initial placement on a centered ellipse so the settled
// layout is reproducible run-to-run and the cluster lands center-canvas.
nodes.forEach((d, i) => {
  const a = (i / nodes.length) * Math.PI * 2 - Math.PI / 2;
  d.x = W / 2 + Math.cos(a) * 240;
  d.y = H / 2 + Math.sin(a) * 170;
});

// Force simulation
const sim = d3.forceSimulation(nodes)
  .force('link', d3.forceLink(links).id(d => d.id).distance(150))
  .force('charge', d3.forceManyBody().strength(-720))
  .force('center', d3.forceCenter(W / 2, H / 2))
  .force('collision', d3.forceCollide().radius(d => d.r + 15));

// Run to completion synchronously (critical for screenshot capture)
for (let i = 0; i < 300; i++) sim.tick();
sim.stop();

// Scale-to-fit: stretch the settled graph into a strong composition box.
const padX = 70;
const padY = 56;
const minX = d3.min(nodes, d => d.x - d.r);
const maxX = d3.max(nodes, d => d.x + d.r);
const minY = d3.min(nodes, d => d.y - d.r);
const maxY = d3.max(nodes, d => d.y + d.r);
const scaleX = (W - padX * 2) / Math.max(1, maxX - minX);
const scaleY = (H - padY * 2) / Math.max(1, maxY - minY);
const cx = (minX + maxX) / 2;
const cy = (minY + maxY) / 2;
nodes.forEach(d => {
  d.x = (d.x - cx) * scaleX + W / 2;
  d.y = (d.y - cy) * scaleY + H / 2;
  d.r = d.r * Math.min(Math.min(scaleX, scaleY), 1.26);
});

// Draw links
svg.selectAll('.link').data(links).join('line')
  .attr('class', 'link')
  .attr('x1', d => d.source.x).attr('y1', d => d.source.y)
  .attr('x2', d => d.target.x).attr('y2', d => d.target.y);

// Draw node shadows (Neo-Brutalism hard shadow)
svg.selectAll('.shadow').data(nodes).join('circle')
  .attr('cx', d => d.x + 4).attr('cy', d => d.y + 4).attr('r', d => d.r)
  .attr('fill', '#0a0a0a').attr('opacity', 0.1);

// Draw nodes
svg.selectAll('.node').data(nodes).join('circle')
  .attr('class', 'node')
  .attr('cx', d => d.x).attr('cy', d => d.y).attr('r', d => d.r)
  .attr('fill', d => groupColor[d.group]);

// Draw labels
svg.selectAll('.label').data(nodes).join('text')
  .attr('class', 'label')
  .attr('x', d => d.x).attr('y', d => d.y)
  .text(d => d.id);
</script>
</body>
```

Notes: D3 v7을 CDN에서 로드. 시뮬레이션 **전에** 노드를 중앙 타원에 결정론적으로 초기 배치해 매 렌더의 레이아웃을 재현 가능하게 하고 클러스터가 캔버스 중앙에 오게 한다(랜덤 초기화는 우하단이 비는 배치를 낳는다). `for (let i=0; i<300; i++) sim.tick(); sim.stop();`으로 시뮬레이션을 동기 실행 — 스크린샷 캡처 시 레이아웃이 안정된 상태 보장. 그 다음 **scale-to-fit pass**로 bounds를 다시 계산해 그래프를 composition box에 채운다. 정사각형 그래프가 16:9 캔버스에서 작아 보이면 `scaleX`와 `scaleY`를 **독립적으로** 계산해 가로와 세로를 각각 채우는 편이 낫다. 링크는 연회색이면 25% 축소에서 노드만 떠 보이므로 **짙은 회색(`#404040`) + `stroke-width:3`**으로 그린다. `nodes`의 `group`으로 색상 분류, `r`로 노드 크기 (중요도). `links`의 `source`/`target`은 노드 `id` 참조. Hard shadow는 동일 좌표에 offset된 검정 원으로 구현.

---

## 22. Typographic Statement (SVG 인라인)

Best for: 에디토리얼 인용, 핵심 정의, 선언적 메시지, 한 문장으로 임팩트

Approach: **SVG inline** — `<text>` + `<tspan>` 정밀 배치. 장식적 큰따옴표 + Neo-Brutalism 카드.

Max: **primary text max 8단어**, attribution max 4단어. 총 ~12단어.

```html
<body>
<svg viewBox="0 0 1440 810" xmlns="http://www.w3.org/2000/svg"
     style="width:1440px;height:810px;background:#f5f5f5">
  <defs>
    <style>
      text { font-family: 'Noto Sans KR', sans-serif; fill: #0a0a0a; }
      .attr { font-family: 'JetBrains Mono', monospace; fill: #616161; }
    </style>
    <pattern id="dots" width="16" height="16" patternUnits="userSpaceOnUse">
      <circle cx="8" cy="8" r="1" fill="rgba(10,10,10,0.06)"/>
    </pattern>
  </defs>
  <rect width="1440" height="810" fill="url(#dots)"/>

  <!-- Card: white rect + 3px border + hard shadow -->
  <rect x="274" y="194" width="900" height="380" rx="0" fill="#0a0a0a" opacity="0.08"/>
  <rect x="270" y="190" width="900" height="380" rx="0" fill="white" stroke="#0a0a0a" stroke-width="3"/>

  <!-- Decorative quote mark: on TOP of card, top-left corner, inside the border -->
  <text x="312" y="452" font-family="Georgia, serif" font-size="240" font-weight="700" fill="#0a0a0a" opacity="0.07">&#8220;</text>

  <!-- Highlight bar: background BEHIND key line, aligned to its glyph body -->
  <rect x="502" y="392" width="436" height="46" fill="#FFE58A" opacity="0.7"/>

  <!-- Primary text (multi-line with tspan), vertically centered in card -->
  <text x="720" y="360" text-anchor="middle" font-size="56" font-weight="900">
    <tspan x="720" dy="0">사용자가 말하는 것과</tspan>
    <tspan x="720" dy="72">실제 행동은 다르다</tspan>
  </text>

  <!-- Attribution -->
  <text class="attr" x="720" y="640" text-anchor="middle" font-size="24" font-weight="700">— Jakob Nielsen</text>
</svg>
</body>
```

Notes: 장식적 큰따옴표(Georgia, opacity 0.07)는 카드 **위에** 그려 top-left corner 워터마크로 두되 카드 보더 안쪽에 배치한다 — 보더에 걸치면 흰 카드에 잘려 흐릿해진다. Neo-Brutalism 카드: white rect + 3px border + 4px offset hard shadow. 인용문은 카드의 **수직·수평 정중앙**에 배치한다. 강조 바(highlight bar)는 텍스트를 **가로지르는 취소선이 아니라** 핵심 라인 뒤 배경으로, 텍스트보다 먼저 그리고 해당 라인의 glyph body(폭·높이)에 맞춘다 (`#FFE58A` yellow). `<tspan>`으로 multi-line 텍스트 구현. Attribution은 JetBrains Mono. 텍스트 길이에 따라 short (1줄, 120px) vs medium (2줄, 56px) 선택.

---
